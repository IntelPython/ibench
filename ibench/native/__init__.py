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
from . import qr

local_benchmarks = {
    'dot_native': dot.Dot_native,
    'det_native': det.Det_native,
    'inv_native': inv.Inv_native,
    'lu_native': lu.Lu_native,
    'cholesky_native': cholesky.Cholesky_native,
    'qr_native': qr.Qr_native
}

# add to the list of benchmark options
benchmarks.update(local_benchmarks)
benchmark_groups['native'] = local_benchmarks
