import sh
from os.path import join
from pathlib import Path
from multiprocessing import cpu_count
import shutil
import copy
import toml

from pythonforandroid.logger import (shprint, info, logger, debug)
from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory

class PyQt5Recipe(Recipe):
    version = '5.15.6'
    url = "https://pypi.python.org/packages/source/P/PyQt5/PyQt5-{version}.tar.gz"
    name = 'pyqt5'

    depends = ['qt5', 'pyjnius', 'setuptools', 'pyqt5sip', 'hostpython3', 'pyqt_builder']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        recipe = self.get_recipe('qt5', self.ctx)
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

            hostpython = self.get_recipe('hostpython3', self.ctx)
            pythondir = hostpython.get_path_to_python()
            site_packages = join(pythondir, 'Lib', 'site-packages')
            env = copy.copy(env)
            env['PYTHONPATH'] = f'{site_packages}:' + env.get('PYTHONPATH', '')

            buildcmd = sh.Command(self.ctx.hostpython)
            # buildcmd = buildcmd.bake('-m', 'sipbuild.tools.install')
            sip_install = join(pythondir, 'usr', 'local', 'bin', 'sip-install')
            buildcmd = buildcmd.bake(sip_install)
            buildcmd = buildcmd.bake('--confirm-license', '--qt-shared', '--verbose')
            buildcmd = buildcmd.bake('--no-tools', '--no-qml-plugin', '--no-designer-plugin', '--no-dbus-python')

            for include in "Qt QtCore QtNetwork QtGui QtQml QtQuick QtAndroidExtras".split(' '):
                buildcmd = buildcmd.bake('--enable', include)

            shprint(buildcmd, _env=env, _tail=50, _critical=True)

recipe = PyQt5Recipe()
