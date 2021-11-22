import sh
from os.path import join
from multiprocessing import cpu_count

from pythonforandroid.logger import (shprint, info, logger, debug)
from pythonforandroid.recipe import CythonRecipe, Recipe, PythonRecipe
from pythonforandroid.toolchain import current_directory

class PyQt5SipRecipe(PythonRecipe):
    version = '12.9.0'
    url = 'https://files.pythonhosted.org/packages/b1/40/dd8f081f04a12912b65417979bf2097def0af0f20c89083ada3670562ac5/PyQt5_sip-12.9.0.tar.gz'
    name = 'pyqt5sip'

    depends = ['setuptools']

    call_hostpython_via_targetpython = False
    site_packages_name = 'PyQt5.sip'


recipe = PyQt5SipRecipe()
