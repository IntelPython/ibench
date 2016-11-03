import numpy as np
import scipy

import ibench
from ibench.benchmarks.bench import Bench

class Det(Bench):

    def _ops(self, n):
        return 2./3.*n*n*n*1e-9

    def _make_args(self, n):
        self._A = np.asfortranarray(np.random.rand(n,n), dtype=self._dtype)

    def _compute(self):
        scipy.linalg.det(self._A, overwrite_a=True, check_finite=False)

ibench.benchmark_map['det'] = globals()['Det']
