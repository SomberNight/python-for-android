from pythonforandroid.recipe import PyProjectRecipe


class PackagingRecipe(PyProjectRecipe):
    version = "26.0"
    url = "https://pypi.python.org/packages/source/p/packaging/packaging-{version}.tar.gz"
    depends = ["setuptools"]

    call_hostpython_via_targetpython = False
    install_in_hostpython = True
    install_in_targetpython = False


recipe = PackagingRecipe()
