# Copyright (C) 2016-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

from . import cholesky
from . import det
from . import dot
from . import fft
from . import inv
from . import lu
from . import qr
from . import svd
from . import blacksch
from . import rng
from . import lregression
from . import lregressionfit
from . import ridge
from . import ridgefit
from . import cosine
from . import corr
from . import svm
from . import kmeans
from . import kmeansfit
from . import eig

benchmarks = {
    'cholesky': cholesky.Cholesky,
    'det': det.Det,
    'dot': dot.Dot,
    'fft': fft.Fft,
    'inv': inv.Inv,
    'lu': lu.Lu,
    'qr': qr.Qr,
    'eig': eig.Eig,
    'svd': svd.Svd,
    'blacksch':blacksch.Blacksch,
    'rng':rng.Rng,
    'lregression':lregression.Lregression,
    'lregressionfit': lregressionfit.Lregressionfit,
    'ridge':ridge.Ridge,
    'ridgefit':ridgefit.Ridgefit,
    'cosine':cosine.Cosine,
    'corr':corr.Corr,
    'svm':svm.Svm,
    'kmeans':kmeans.Kmeans,
    'kmeansfit':kmeansfit.Kmeansfit
}

benchmark_groups = {
    'linalg': ['cholesky', 'det', 'dot', 'inv', 'lu', 'qr', 'svd', 'eig'],
    'all': list(benchmarks.keys()),
    'sklearn': ['lregression', 'lregressionfit', 'ridge', 'ridgefit',
                'cosine','corr','svm','kmeans','kmeansfit'],
    'bench2018': ['fft', 'lu', 'dot', 'cholesky', 'qr', 'eig', 'blacksch',
                  'rng', 'lregression', 'lregressionfit', 'ridge',
                  'ridgefit','cosine','corr','svm','kmeans','kmeansfit']
}

# Try to get native benchmarks
try:
    from .. import native
except ImportError:
    pass
