from pythonforandroid.recipe import PythonRecipe


class TomlRecipe(PythonRecipe):
    version = "0.10.2"
    url = "https://pypi.python.org/packages/source/t/toml/toml-{version}.tar.gz"
    depends = ["setuptools"]

    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = TomlRecipe()
