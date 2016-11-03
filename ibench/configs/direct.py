import sys

import ibench
from ibench.configs.config import Config

class Direct(Config):
    '''Run with same python interpreter as invoked the script'''
    _python_path = sys.executable

ibench.config_map['direct'] = globals()['Direct']
