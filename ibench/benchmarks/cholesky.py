import numpy as np
import scipy.linalg

from .bench import Bench

class Cholesky(Bench):
    sizes = {'large': 40000, 'small': 10000, 'test': 2}

    def _ops(self, n):
        return n*n*n/3.0*1e-9

    def _make_args(self, n):
        self._A = np.asarray(np.random.rand(n,n), dtype=self._dtype)
        self._A = np.asfortranarray(self._A*self._A.transpose() + n*np.eye(n))

    def _compute(self):
        scipy.linalg.cholesky(self._A, lower=False, overwrite_a=True, check_finite=False)
