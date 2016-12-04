import sys

from  .config import Config

class Direct(Config):
    '''Run with same python interpreter as invoked the script'''
    _python_path = sys.executable
