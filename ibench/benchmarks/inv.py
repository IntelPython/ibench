import numpy as np
import scipy

import ibench
from ibench.benchmarks.bench import Bench

class Inv(Bench):

    def _ops(self, n):
        # scipy is getrf getri
        return 2.*n*n*n*1e-9
        # numpy calls gesv
        # lu + triangular solve
        # TRF + TRS
        # 2/3 n^3 + 2 n^3 = 8/3 n^3
        # return 8./3.*N*N*N*1e-9

    def _make_args(self, n):
        self._A = np.asfortranarray(np.random.rand(n,n), dtype=self._dtype)

    def _compute(self):
        scipy.linalg.inv(self._A, overwrite_a=True, check_finite=False)

ibench.benchmark_map['inv'] = globals()['Inv']
