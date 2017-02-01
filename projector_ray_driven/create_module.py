from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("radon_ray_driven",
                             sources=[ "radon_ray_driven.pyx" ,
                                       "radon_rd.c" 
                                       ],
                             include_dirs=[numpy.get_include()],libraries=['gcov'],
    extra_compile_args=['-w','-O3','-march=native','-ffast-math','-fprofile-generate','-fopenmp'],extra_link_args=['-fprofile-generate'])],
)
