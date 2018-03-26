import numpy as np

from .bench import Bench

try:
    import numpy.random_intel as rnd
except:
    import numpy.random as rnd
    
class Rng(Bench):

    sizes = {'large': 10000, 'small': 1000, 'tiny': 100, 'test': 2}

    def _ops(self, n):
        # TODO: Needs a more accurate count
        return 2E-9 * n

    def _sample_uniform(self, rs, sz):
        rs.uniform(-1, 1, size=sz)
        
    def _make_args(self, n):
        self._rs = rnd.RandomState(123)
        # rnd.RandomState(123, brng='MT19937') with the Intel variant in the future
        self._size = n 

    def _compute(self):
        self._sample_uniform(self._rs, (self._size * 100, 1000))
