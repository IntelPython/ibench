import numpy as np
import sklearn
import multiprocessing
from numpy.random import rand
from sklearn.metrics.pairwise import pairwise_distances

from .bench import Bench

if sklearn.__version__ == '0.18.2':
    sklearn.utils.validation._assert_all_finite = lambda X: None 

class Corr(Bench):
    """
    Benchmark for Correlation Distance from Scikit-learn
    Attempts to utilize parallelism for larger datasets
    """
    sizes = {'large': 10000, 'small': 5000, 'tiny': 1000, 'test': 10}

    def _ops(self, n):
        return 2E-9 * n

    def _make_args(self, n):
        p = int(n/10)
        self._X = rand(p,n)
            
    def _compute(self):
        self._cor_dist = pairwise_distances(self._X, metric='correlation', n_jobs=-1)
