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

benchmarks = {
    'cholesky': cholesky.Cholesky,
    'det': det.Det,
    'dot': dot.Dot,
    'fft': fft.Fft,
    'inv': inv.Inv,
    'lu': lu.Lu,
    'qr': qr.Qr,
    'svd': svd.Svd,
    'blacksch':blacksch.Blacksch,
    'rng':rng.Rng,
    'lregression':lregression.Lregression,
    'lregressionfit': lregressionfit.Lregressionfit,
    'ridge':ridge.Ridge,
    'ridgefit':ridgefit.Ridgefit,
    'cosine':cosine.Cosine,
    'corr':corr.Corr
}

benchmark_groups = {
    'linalg': ['cholesky', 'det', 'dot', 'inv', 'lu', 'qr', 'svd'],
    'all': list(benchmarks.keys()),
    'sklearn': ['lregression', 'lregressionfit', 'ridge', 'ridgefit',
                'cosine','corr'],
    'bench2018': ['fft', 'lu', 'dot', 'cholesky', 'qr', 'blacksch',
                  'rng', 'lregression', 'lregressionfit', 'ridge',
                  'ridgefit','cosine','corr']
}
