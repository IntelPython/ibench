import numpy as np
import scipy.linalg

from .bench import Bench

class Svd(Bench):
    sizes = {'large': 10000, 'small': 5000, 'tiny': 1000, 'test': 2}

    def _ops(self, n):
        return (4./3.)*n*n*n*1e-9

    def _make_args(self, n):
        self._A = np.asarray(np.random.rand(n,n), dtype=self._dtype)

    def _compute(self):
        scipy.linalg.svd(self._A, overwrite_a=True, check_finite=False, full_matrices=False)
