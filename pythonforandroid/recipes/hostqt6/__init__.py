from os.path import join, isfile
from os import environ
from multiprocessing import cpu_count
import sh

from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory
from pythonforandroid.logger import info, debug, shprint
from pythonforandroid.util import ensure_dir

from pythonforandroid.recipes.qt6 import Qt6Recipe


class HostQt6Recipe(Recipe):
    r = Qt6Recipe()
    info(r.version)
    info(r.url)
    name = 'hostqt6'
    # version = Qt6Recipe.version #'6.4.3'
    version = '6.4.3'
    # url = Qt6Recipe.url #'https://download.qt.io/archive/qt/6.4/{version}/single/qt-everywhere-src-{version}.zip'
    url = 'https://download.qt.io/archive/qt/6.4/{version}/single/qt-everywhere-src-{version}.zip'

    build_subdir = 'native-build'

    built_libraries = {}

    def get_recipe_env(self, arch=None, with_flags_in_cc=True, with_python=True):
        env = environ.copy()
        return env

    def should_build(self, arch):
        # if Path(self.python_exe).exists():
        #     # no need to build, but we must set hostpython for our Context
        #     self.ctx.hostpython = self.python_exe
        #     return False
        return not isfile(join(self.get_install_dir(), 'bin', 'qmake'))

    def get_build_container_dir(self, arch=None):
        # choices = self.check_recipe_choices()
        # dir_name = '-'.join([self.name] + choices)
        return join(self.ctx.build_dir, 'other_builds', self.name)

    def get_build_dir(self, arch=None):
        '''
        .. note:: Unlike other recipes, the hostqt6 build dir doesn't
            depend on the target arch
        '''
        return join(self.get_build_container_dir(), self.build_subdir)

    def get_install_dir(self):
        return join(self.get_build_dir(), 'install')

    def build_arch(self, arch):
        # super().build_arch(arch)
        env = self.get_recipe_env(arch)

        build_dir = self.get_build_dir(arch.arch)
        ensure_dir(build_dir)
        install_dir = self.get_install_dir()
        ensure_dir(install_dir)

        with current_directory(build_dir):
            info("compiling host qt6 from sources")
            debug("environment: {}".format(env))

            # wtf
            shprint(sh.Command('dos2unix'), 'configure')
            shprint(sh.Command('dos2unix'), 'qtbase/configure')

            configure = sh.Command('./configure')
            # options?
            shprint(configure, '--help', _env=env, _tail=50, _critical=True)

            configure = configure.bake('-opensource', '-confirm-license', '-disable-rpath')
            # configure = configure.bake('-extprefix', self.ctx.libs_dir)
            configure = configure.bake('-prefix', install_dir)

            configure = configure.bake('-nomake', 'tests')
            configure = configure.bake('-nomake', 'examples')
            configure = configure.bake('-make', 'tools')
            configure = configure.bake('-submodules', ','.join(
                ['qtbase', 'qttools']))
            configure = configure.bake('-skip', ','.join(
                ['qtactiveqt']))

            info(str(configure))

            shprint(configure, _tail=50, _critical=True)

            shprint(sh.make, '-j' + str(cpu_count()), _critical=True)
            shprint(sh.make, '-j' + str(cpu_count()), 'install', _critical=True)


recipe = HostQt6Recipe()
