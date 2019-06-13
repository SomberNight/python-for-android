import os

from pythonforandroid.recipe import PythonRecipe


class PycryptodomexRecipe(PythonRecipe):
    version = '3.6.4'
    url = 'https://github.com/SomberNight/pycryptodome/archive/{version}.tar.gz'
    depends = ['setuptools', 'cffi']


recipe = PycryptodomexRecipe()
