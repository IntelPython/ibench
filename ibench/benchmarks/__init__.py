from . import cholesky
from . import det
from . import dot
from . import fft
from . import inv
from . import lu
from . import qr
from . import svd

benchmarks = {
    'cholesky': cholesky.Cholesky,
    'det': det.Det,
    'dot': dot.Dot,
    'fft': fft.Fft,
    'inv': inv.Inv,
    'lu': lu.Lu,
    'qr': qr.Qr,
    'svd': svd.Svd
}

benchmark_groups = {
    'linalg': ['cholesky', 'det', 'dot', 'inv', 'lu', 'qr', 'svd'],
    'all': list(benchmarks.keys())
}
