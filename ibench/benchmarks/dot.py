import ibench
from ibench.benchmarks.bench import Bench
import numpy as np

class Dot(Bench):
    size = 40000
    _LARGEDIM = 20000

    def _ops(self, n):
        return 2E-9 * self._LARGEDIM * self._LARGEDIM*n

    def _make_args(self, n):
        self._A = np.asarray(np.random.rand(self._LARGEDIM, n), dtype=self._dtype)
        self._B = np.asarray(np.random.rand(n, self._LARGEDIM), dtype=self._dtype)
        self._C = np.asarray(np.random.rand(self._LARGEDIM, self._LARGEDIM), dtype=self._dtype)

    def _compute(self):
        self._A.dot(self._B, out=self._C)
