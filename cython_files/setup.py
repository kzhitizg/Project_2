from setuptools import setup
from Cython.Build import cythonize

import numpy

setup(
    name='Example code',
    ext_modules=cythonize("example.pyx", build_dir = "build"),
    zip_safe=False,
    include_dirs = [numpy.get_include()]
)