from pythonforandroid.recipe import PythonRecipe


class SipRecipe(PythonRecipe):
    version = '6.8.1'
    url = "https://pypi.python.org/packages/source/s/sip/sip-{version}.tar.gz"
    name = 'sip'

    depends = ['setuptools', 'packaging', 'tomli']

    call_hostpython_via_targetpython = False
    install_in_hostpython = True
    install_in_targetpython = False  # FIXME broken
    site_packages_name = 'sipbuild'


recipe = SipRecipe()
