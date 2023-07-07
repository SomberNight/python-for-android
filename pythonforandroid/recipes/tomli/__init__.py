from pythonforandroid.recipe import PythonRecipe

from pythonforandroid.logger import shprint, info
from pythonforandroid.util import current_directory
import sh
from os.path import join, dirname


class TomliRecipe(PythonRecipe):
    version = "2.0.1"
    url = "https://pypi.python.org/packages/source/t/tomli/tomli-{version}.tar.gz"
    depends = ['setuptools']
    # setup_extra_args = []
    site_packages_name = 'tomli'

    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def build_arch(self, arch):
        '''Install the Python module by calling setup.py install with
        the target Python dir.'''
        with current_directory(join(self.get_build_dir(arch.arch))):
            rdir = join(self.ctx.root_dir, 'recipes', self.name)
            shprint(sh.cp, '-t', '.', join(rdir, 'setup.py'))
        super().build_arch(arch)
        info(str(self.get_recipe_env(arch)))
        # self.install_python_package(arch)

    def install_python_package(self, arch, name=None, env=None, is_dir=True):
        '''Automate the installation of a Python package (or a cython
        package where the cython components are pre-built).'''
        # arch = self.filtered_archs[0]  # old kivy-ios way
        if name is None:
            name = self.name
        if env is None:
            env = self.get_recipe_env(arch)

        info('Installing {} into site-packages'.format(self.name))

        info(f'HOST PYTHON={self.hostpython_location}')
        hostpython = sh.Command(self.hostpython_location)
        hpenv = env.copy()
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(hostpython, 'setup.py', 'install', '-O2',
                    '--root={}'.format(self.ctx.get_python_install_dir(arch.arch)),
                    '--install-lib=.',
                    _env=hpenv, *self.setup_extra_args)

            # If asked, also install in the hostpython build dir
            if self.install_in_hostpython:
                self.install_hostpython_package(arch)

    def install_hostpython_package(self, arch):
        env = self.get_hostrecipe_env(arch)
        real_hostpython = sh.Command(self.real_hostpython_location)
        info(f'INSTALLING IN HOST PYTHON, real host python={real_hostpython}')
        shprint(real_hostpython, 'setup.py', 'install', '-O2',
                '--root={}'.format(dirname(self.real_hostpython_location)),
                '--install-lib=Lib/site-packages',
                _env=env, *self.setup_extra_args)


recipe = TomliRecipe()
