# Copyright (C) 2016, 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

# python loads libraries with RTLD_LOCAL, but MKL requires RTLD_GLOBAL
# pre-load MKL with RTLD_GLOBAL before loading the native extension
import ctypes
try:
    ctypes.CDLL('libmkl_rt.so', ctypes.RTLD_GLOBAL)
except OSError:
    raise ImportError

from ibench.benchmarks import benchmarks, benchmark_groups
from . import det
from . import dot
from . import inv
from . import lu
from . import cholesky

local_benchmarks = {
    'dot_native': dot.Dot,
    'det_native': det.Det,
    'inv_native': inv.Inv,
    'lu_native': lu.Lu,
    'cholesky_native': cholesky.Cholesky
}

# add to the list of benchmark options
benchmarks.update(local_benchmarks)
benchmark_groups['native'] = local_benchmarks
