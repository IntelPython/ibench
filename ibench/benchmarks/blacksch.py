import numpy as np
from numpy import log, exp
from .bench import Bench

try:
    import numpy.random_intel as rnd
except:
    import numpy.random as rnd
try:
    from numpy import erf
except:
    from scipy.special import erf
        
try:
    from numpy import invsqrt
    numpy_ver += "-invsqrt"
except:
    invsqrt = lambda x: 1.0/np.sqrt(x)

try:
    xrange
except NameError:
    xrange = range

SEED = 7777777
S0L = 10.0
S0H = 50.0
XL = 10.0
XH = 50.0
TL = 1.0
TH = 2.0
RISK_FREE = 0.1
VOLATILITY = 0.2
TEST_ARRAY_LENGTH = 1024

class Blacksch(Bench):
    sizes = {'large': 200000000, 'small': 100000000, 'tiny': 1000000, 'test': 100}

    def _gen_data(self, nopt):
        return (
            rnd.uniform(S0L, S0H, nopt),
            rnd.uniform(XL, XH, nopt),
            rnd.uniform(TL, TH, nopt),
        )

    def _black_scholes (self, nopt, price, strike, t, rate, vol ):
        mr = -rate
        sig_sig_two = vol * vol * 2

        P = price
        S = strike
        T = t

        a = log(P / S)
        b = T * mr

        z = T * sig_sig_two
        c = 0.25 * z
        y = invsqrt(z)

        w1 = (a - b + c) * y
        w2 = (a - b - c) * y

        d1 = 0.5 + 0.5 * erf(w1)
        d2 = 0.5 + 0.5 * erf(w2)

        Se = exp(b) * S

        call = P * d1 - Se * d2
        put = call - P + Se
    
        return (call, put)

    def _ops(self, n):
        # TODO: Need better ops count here
        return 2E-9 * n*11

    def _make_args(self, n):
        self._nopt=n
        self._price, self._strike, self._t = self._gen_data(self._nopt)
        self._call = np.zeros(self._nopt, dtype=np.float64)
        self._put  = -np.ones(self._nopt, dtype=np.float64)

    def _compute(self):
        self._black_scholes(self._nopt, self._price, self._strike, self._t, RISK_FREE, VOLATILITY)

