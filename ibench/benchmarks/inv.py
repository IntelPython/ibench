# Copyright (C) 2016-2017 Intel Corporation
#
# SPDX-License-Identifier: MIT

import numpy as np
import scipy

from .bench import Bench

class Inv(Bench):
    sizes = {'large': 25000, 'small': 10000, 'tiny': 2000, 'test': 2}

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
        # yes, we overwrite the input here without refreshing it,
        # but because (A**-1)**-1 = A, there shouldn't be any big problems
        # w.r.t. early termination of inverse
        scipy.linalg.inv(self._A, overwrite_a=True, check_finite=False)
