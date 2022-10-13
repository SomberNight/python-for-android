import sh
from os.path import join
from multiprocessing import cpu_count

from pythonforandroid.logger import (shprint, info, logger, debug)
from pythonforandroid.recipe import CythonRecipe, Recipe, PythonRecipe
from pythonforandroid.toolchain import current_directory

class PyQt5SipRecipe(PythonRecipe):
    version = '12.9.0'
    url = "https://pypi.python.org/packages/source/P/PyQt5_sip/PyQt5_sip-{version}.tar.gz"
    name = 'pyqt5sip'

    depends = ['setuptools']

    call_hostpython_via_targetpython = False
    site_packages_name = 'PyQt5.sip'


recipe = PyQt5SipRecipe()
