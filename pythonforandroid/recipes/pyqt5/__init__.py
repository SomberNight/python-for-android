import sh
from os.path import join
from pathlib import Path
from multiprocessing import cpu_count
import toml

from pythonforandroid.logger import (shprint, info, logger, debug)
from pythonforandroid.recipe import CythonRecipe, Recipe
from pythonforandroid.toolchain import current_directory

class PyQt5Recipe(Recipe):
    version = '5.15.6'
    url = 'https://files.pythonhosted.org/packages/3b/27/fd81188a35f37be9b3b4c2db1654d9439d1418823916fe702ac3658c9c41/PyQt5-5.15.6.tar.gz'
    name = 'pyqt5'

    depends = ['qt5', 'pyjnius', 'setuptools', 'pyqt5sip']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        recipe = Recipe.get_recipe('qt5', self.ctx)
        qt5_env = recipe.get_recipe_env(arch)
        env['TARGET_QMAKEPATH'] = qt5_env['TARGET_QMAKEPATH']

        return env

    def update_pyproject_toml(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        project_dict = {}
        with open(join(build_dir, 'pyproject.toml'), 'r') as f:
            project_dict = toml.load(f)

        project_dict['tool']['sip']['project'] = {
            'android-abis': [arch.arch],
            'py-pylib-dir': self.ctx.python_recipe.link_root(arch.arch),
            'py-include-dir': self.ctx.python_recipe.include_root(arch.arch),
            'py-pylib-shlib': 'python{}'.format(self.ctx.python_recipe.link_version),
            'target-dir': self.ctx.get_python_install_dir()
        }

        project_dict['tool']['sip']['bindings'] = {}
        for binding in 'Qt QtCore QtNetwork QtGui QtQml QtQuick QtAndroidExtras'.split(' '):
            project_dict['tool']['sip']['bindings'][binding] = {
                'extra-link-args': [
                    '-L{}'.format(self.ctx.python_recipe.link_root(arch.arch)),
                    '-lpython{}'.format(self.ctx.python_recipe.link_version)
                ],
                'disabled-features': ['PyQt_Desktop_OpenGL']
            }

        with open(join(build_dir, 'pyproject.toml'), 'w') as f:
            toml.dump(project_dict, f)

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        self.update_pyproject_toml(arch)

    def build_arch(self, arch):
        super().build_arch(arch)

        env = self.get_recipe_env(arch)
        env['PATH'] = env['TARGET_QMAKEPATH'] + ":" + env['PATH']
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            info("compiling pyqt5")

            buildcmd = sh.Command('sip-install')
            buildcmd = buildcmd.bake('--confirm-license', '--no-tools', '--qt-shared')

            for include in "Qt QtCore QtNetwork QtGui QtQml QtQuick QtAndroidExtras".split(' '):
                buildcmd = buildcmd.bake('--enable', include)

            shprint(buildcmd, _env=env, _tail=50, _critical=True)

recipe = PyQt5Recipe()
