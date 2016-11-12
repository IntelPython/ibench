import subprocess
import sys

from  ibench.configs.config import Config

class Conda_py2(Config):
    '''py2 conda environment'''
    def build(self):
        subprocess.call('conda env remove -n ibench.py2', shell=True)
        subprocess.check_call('conda create -n ibench.py2 python=2 jinja2 scipy pytest', shell=True)
