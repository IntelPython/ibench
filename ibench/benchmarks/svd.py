# Copyright (C) 2016-2017 Intel Corporation
#
# SPDX-License-Identifier: MIT

import numpy as np
import scipy.linalg

from .bench import Bench


class Svd(Bench):
    sizes = {'large': 10000, 'small': 5000, 'tiny': 1000, 'test': 2}

    def _ops(self, n):
        return (4./3.)*n*n*n*1e-9

    def _make_args(self, n):
        self._A = np.asfortranarray(np.random.rand(n, n), dtype=self._dtype)

    def _compute(self):
        # We specify overwrite_a=False here because once the input array
        # is overwritten, dgesdd might decide to terminate early
        scipy.linalg.svd(self._A, overwrite_a=False, check_finite=False)
