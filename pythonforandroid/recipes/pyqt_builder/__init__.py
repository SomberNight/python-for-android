from pythonforandroid.recipe import PythonRecipe

class PyQtBuilderRecipe(PythonRecipe):
    version = '1.12.2'
    url = "https://pypi.python.org/packages/source/P/PyQt-builder/PyQt-builder-{version}.tar.gz"
    name = 'pyqt_builder'

    depends = ['sip', 'packaging']

    call_hostpython_via_targetpython = False
    install_in_hostpython = True
    install_in_targetpython = False  # FIXME broken
    site_packages_name = 'pyqtbuild'


recipe = PyQtBuilderRecipe()
