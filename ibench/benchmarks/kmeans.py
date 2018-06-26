import numpy as np
import sklearn
import multiprocessing
from numpy.random import rand
from sklearn.cluster import KMeans

from .bench import Bench

if sklearn.__version__ == '0.18.2':
    sklearn.utils.validation._assert_all_finite = lambda X: None 

class Kmeans(Bench):
    """
    Benchmark for Kmeans Training from Scikit-learn
    Attempts to utilize parallelism for larger datasets
    """
    sizes = {'large': 1000000, 'small': 100000, 'tiny': 10000, 'test': 1000}

    def _ops(self, n):
        return 2E-9 * n*n*n

    def _make_args(self, n):
        p = int(np.log(n)+100)
        self._X = rand(n,p)
        self._kmeans = KMeans(n_clusters=10, n_jobs=int(-1), n_init=1)

    def _compute(self):
        self._trained_model =  self._kmeans.fit(self._X)
