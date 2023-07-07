from pythonforandroid.recipe import PythonRecipe


class PlyRecipe(PythonRecipe):
    version = '3.11'
    url = "https://pypi.python.org/packages/source/p/ply/ply-{version}.tar.gz"
    name = 'ply'

    depends = ['packaging']

    call_hostpython_via_targetpython = False
    install_in_hostpython = True
    site_packages_name = 'ply'


recipe = PlyRecipe()
