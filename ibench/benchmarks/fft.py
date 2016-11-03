import math
import numpy as np
import scipy.fftpack

import ibench
from ibench.benchmarks.bench import Bench

class FFT(Bench):
    # If you change the value of runs, change native.cpp as well
    _runs = 1000

    def _ops(self, n):
        # This is not an actual flop count; it is simply a convenient scaling,
        # based on the fact that the radix-2 Cooley-Tukey algorithm asymptotically
        # requires 5 N log2(N) floating-point operations.
        # http://www.fftw.org/speed/method.html
        return self._runs*5*n*math.log(n,2)*1e-9

    def _make_args(self, n):
        self._A = np.asarray(np.random.rand(n), dtype=np.complex128)

    def _compute(self):
        for i in range(self._runs):
            scipy.fftpack.fft(self._A, overwrite_x = True)

ibench.benchmark_map['fft'] = globals()['FFT']
