import numpy as np
import scipy

from .bench import Bench

class Lu(Bench):
    sizes = {'large': 35000, 'small': 20000, 'tiny': 5000, 'test': 2}

    def _ops(self, n):
        return 2./3.*n*n*n*1e-9

    def _make_args(self, n):
        self._A = np.asfortranarray(np.asarray(np.random.rand(n,n), dtype=self._dtype))

    def _compute(self):
        scipy.linalg.lu(a=self._A, overwrite_a=True, check_finite=False)
