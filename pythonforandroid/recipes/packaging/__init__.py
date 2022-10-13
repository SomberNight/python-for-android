from pythonforandroid.recipe import PythonRecipe


class PackagingRecipe(PythonRecipe):
    version = "21.3"
    url = "https://pypi.python.org/packages/source/p/packaging/packaging-{version}.tar.gz"
    depends = ["setuptools", "pyparsing"]

    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = PackagingRecipe()
