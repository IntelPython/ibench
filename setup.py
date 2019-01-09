# Copyright (C) 2016, 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import print_function
from setuptools import setup


def build_native():
    '''Return cythonized extensions for native benchmarks'''
    try:
        # use icc if it is available
        icc = subprocess.check_output('which icc',shell=True).decode('utf-8')
    except:
        icc = None
        extra_args = []
    else:
        print('Using icc: %s' % icc)
        os.environ['CC'] = icc
        os.environ['CXX'] = os.environ['CC']
        extra_args = ['-mkl']

    if not 'CXX' in os.environ:
        print('icc not detected, and CXX is not set. Skipping building native benchmarks.')
        print('If you want to build native benchmarks, specify a compiler in the CXX '
              'environment variable.')
        return

    try:
        os.mkdir('pyx')
    except OSError:
        pass

    def make_bench(name):
        tpl_env = Environment(loader=FileSystemLoader('ibench/native'))
        with open('pyx/%s.pyx' % name,'w') as pyxf:
            pyxf.write(tpl_env.get_template('tpl.bench.pyx').render({'bench': name, 'Bench': name.capitalize()}))
        return Extension(name='ibench.native.%s' % name,
                         extra_compile_args=extra_args,
                         extra_link_args=extra_args,
                         sources=['pyx/%s.pyx' % name])

    return cythonize([make_bench(i) for i in ['det', 'dot', 'inv', 'lu', 'cholesky', 'qr']])


packages = ['ibench','ibench/docker','ibench/cmds','ibench/configs','ibench/benchmarks']


try:
    from Cython.Build import cythonize
    from jinja2 import FileSystemLoader
    from jinja2 import Environment
    import os
    from setuptools import Extension
    import subprocess
    import sys
except ImportError:
    print('Cython not found. Skipping building native benchmarks.')
    extensions = None
else:
    # Cython and Jinja2 found in build environment. Look for compilers
    extensions = build_native()
    if extensions:
        packages.append('ibench/native')


setup(name='ibench',
      version='0.1rc',
      description='Benchmarking for scientific python',
      url='http://github.com/intelpython/ibench',
      download_url='http://github.com/intelpython/ibench/tarball/0.1rc',
      author='Robert Cohn',
      author_email='Robert.S.Cohn@intel.com',
      license='MIT',
      packages=packages,
      install_requires=['jinja2','numpy','scipy','scikit-learn'],
      ext_modules=extensions,
      package_data={'ibench': ['docker/Dockerfile.tpl']},
      zip_safe=False)
