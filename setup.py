from setuptools import setup

setup(name='ibench',
      version='0.1',
      description='Benchmarking for scientific python',
      url='http://github.com/rscohn2/ibench',
      author='Robert Cohn',
      author_email='Robert.S.Cohn@intel.com',
      license='MIT',
      packages=['ibench'],
      package_data={'ibench': ['Dockerfile.tpl']},
      zip_safe=False)
