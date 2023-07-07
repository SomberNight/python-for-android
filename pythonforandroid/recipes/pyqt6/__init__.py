import sh
from os.path import join
from pathlib import Path
import copy
import toml

from pythonforandroid.logger import shprint, info
from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory


class PyQt6Recipe(Recipe):
    version = '6.4.2'
    url = "https://pypi.python.org/packages/source/P/PyQt6/PyQt6-{version}.tar.gz"
    name = 'pyqt6'

    depends = ['qt6', 'pyjnius', 'setuptools', 'pyqt6sip', 'hostpython3', 'pyqt_builder']

    # BINDINGS = ['Qt', 'QtCore', 'QtNetwork', 'QtGui', 'QtQml', 'QtQuick', 'QtAndroidExtras']
    BINDINGS = ['QtCore', 'QtNetwork', 'QtGui', 'QtQml', 'QtQuick']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)

        recipe = self.get_recipe('hostqt6', self.ctx)
        env['LD_LIBRARY_PATH'] = join(recipe.get_install_dir(), 'lib')
        # env['HOSTQT_PATH'] = join(recipe.get_install_dir(), 'bin')

        recipe = self.get_recipe('qt6', self.ctx)
        qt6_env = recipe.get_recipe_env(arch)
        env['QT_EXT_PATH'] = qt6_env['QT_EXT_PATH']

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
            'target-dir': self.ctx.get_python_install_dir(arch.arch)
        }

        project_dict['tool']['sip']['bindings'] = {}
        for binding in self.BINDINGS:
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
        env['PATH'] = env['QT_EXT_PATH'] + ":" + env['PATH']
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            info("compiling pyqt6")

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

            for include in self.BINDINGS:
                buildcmd = buildcmd.bake('--enable', include)

            shprint(buildcmd, _env=env, _tail=50, _critical=True)

            with open(join(build_dir, 'compile_finished'), 'w') as fp:
                fp.write('')

    def should_build(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        return not Path(join(build_dir, 'compile_finished')).is_file()


recipe = PyQt6Recipe()
