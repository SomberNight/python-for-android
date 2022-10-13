from pythonforandroid.recipe import PythonRecipe


class PyparsingRecipe(PythonRecipe):
    version = "3.0.7"
    url = "https://pypi.python.org/packages/source/p/pyparsing/pyparsing-{version}.tar.gz"
    depends = ["setuptools"]
    
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = PyparsingRecipe()
