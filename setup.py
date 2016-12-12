from setuptools import setup

setup(name='ibench',
      version='0.1rc',
      description='Benchmarking for scientific python',
      url='http://github.com/intelpython/ibench',
      download_url='http://github.com/intelpython/ibench/tarball/0.1rc',
      author='Robert Cohn',
      author_email='Robert.S.Cohn@intel.com',
      license='MIT',
      packages=['ibench','ibench/docker','ibench/cmds','ibench/configs','ibench/benchmarks'],
      install_requires=['jinja2','numpy','scipy'],
      package_data={'ibench': ['docker/Dockerfile.tpl']},
      zip_safe=False)
