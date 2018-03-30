import numpy as np
import sklearn, sklearn.utils
import sklearn.svm as svm
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score

from .bench import Bench

sklearn._ASSUME_FINITE = True

if sklearn.__version__ == '0.18.2':
    sklearn.utils.validation._assert_all_finite = lambda X: None 

features = [10, 50, 100, 200, 400, 800, 1000]
vectors = [1000, 2000, 4000, 10000]

class Svm(Bench):
    """
    Benchmark for Ridge Regression Prediction from Scikit-learn
    Attempts to utilize parallelism for larger datasets
    """
    sizes = {'large': 4, 'small': 3, 'tiny': 2, 'test': 1}
    
    def _gen_datasets(self, features, vectors, classes, dest='data'):
        """Generate classification datasets in binary .npy files
        features: a list of feature lengths to test
        vectors: a list of sample lengths to test
        classes: number of classes (2 for binary classification dataset)
        """
        self._X, self._y = make_classification(n_samples=vectors, n_features=features, n_informative=features, n_redundant=0, n_classes=classes, random_state=0)
        return self._X, self._y

    def _ops(self, n):
        return 2E-9 * n

    def _make_args(self, n):
        self._X, self._y = self._gen_datasets(features[n-1],vectors[n-1],2)
        self._clf = svm.SVC(C=0.01, kernel='linear', max_iter=10000, tol=1e-16, shrinking=True)

    def _compute(self):
        self._clf.fit(self._X, self._y)
