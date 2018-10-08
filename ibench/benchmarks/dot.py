# Copyright (C) 2016-2017 Intel Corporation
#
# SPDX-License-Identifier: MIT

import numpy as np

from .bench import Bench

class Dot(Bench):
    sizes = {'large': 10000, 'small': 5000, 'tiny': 1000, 'test': 2}

    def _ops(self, n):
        return 2E-9 * n*n*n

    def _make_args(self, n):
        self._A = np.asarray(np.random.rand(n, n), dtype=self._dtype)
        self._B = np.asarray(np.random.rand(n, n), dtype=self._dtype)
        self._C = np.asarray(np.random.rand(n, n), dtype=self._dtype)

    def _compute(self):
        self._A.dot(self._B, out=self._C)
