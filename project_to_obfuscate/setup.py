
from pathlib import Path
from setuptools import setup
from Cython.Build import cythonize

THIS_DIR = Path(__file__).parent

setup(
    name='Hello world app',
    ext_modules=cythonize("some_package/mod4.pyx")
)
