from setuptools import setup, Extension
from Cython.Build import cythonize

import numpy

setup(
    name='Hello world app',
    ext_modules=cythonize(Extension(
           "NbrRegionSegment",                    # the extension name
           sources=["./src/cython/NbrRegionSegment.pyx", "./src/cpp/NbrRegionSegment.cpp"],      # the Cython source and
           language="c++",                          # generate and compile C++ code
      )),
    zip_safe=False,
    include_dirs = [numpy.get_include()]
)