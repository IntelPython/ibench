from setuptools import setup

setup(name='ibench',
      version='0.1',
      description='Benchmarking for scientific python',
      url='http://github.com/rscohn2/ibench',
      author='Robert Cohn',
      author_email='Robert.S.Cohn@intel.com',
      license='MIT',
      packages=['ibench'],
      install_requires=['jinja2','numpy','scipy'],
      package_data={'ibench': ['docker/Dockerfile.tpl']},
      zip_safe=False)
