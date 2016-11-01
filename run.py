import subprocess
import json
import datetime
import sys
import numpy as np
import time
import gc
import os.path
import os
import platform
import scipy
import scipy.fftpack
import scipy.linalg
import math
import argparse

results = {}

dtype = np.double

def log(message):
    if args.q:
        return
    print(message)
    
class Bench:
    def __init__(self):
        self.name = self.__class__.__name__
        
    def log(self, message):
        log('%s: %s' % (self.name,message))

    def run(self, n, runs):
        self.make_args(n)

        gcold = gc.isenabled()
        gc.disable()

        times = []
        for i in range(runs):
            t_start = time.time()
            self.compute()
            elapsed = time.time() - t_start
            times.append(elapsed)

        if gcold:
            gc.enable()

        return times

    def measure(self, n, runs):
        self.log('')
        self.log('  N = %d' % n)

        times = self.run(n, runs)

        ops = self.ops(n)
        for elapsed in times:
            self.log('  elapsed %f gflops %f' % (elapsed,ops/elapsed))
                    
        self.summarize(n, times)

    def summarize(self, n, times):
        t = np.asarray(times)
        median = np.median(t)
        ops = self.ops(n)
        self.log('  gflops %f' % (ops/median))
        results['runs'].append({'name': self.name,
                                'N': n,
                                'gflops': ops/median,
                                'ops': ops,
                                'times': times,
                                'stats': {'min': np.amin(t),  'max': np.max(t),  'median': median}})
    
class qr(Bench):
    def ops(self, n):
        return (4./3.)*n*n*n*1e-9

    def make_args(self, n):
        self.A = np.asarray(np.random.rand(n,n), dtype=dtype)

    def compute(self):
        scipy.linalg.qr(self.A, overwrite_a=True, check_finite=False, mode='raw')

class svd(Bench):
    def ops(self, n):
        return (4./3.)*n*n*n*1e-9

    def make_args(self, n):
        self.A = np.asarray(np.random.rand(n,n), dtype=dtype)

    def compute(self):
        scipy.linalg.svd(self.A, overwrite_a=True, check_finite=False, full_matrices=False)

class dot(Bench):
    LARGEDIM = 20000

    def ops(self, n):
        return 2E-9 * self.LARGEDIM * self.LARGEDIM*n

    def make_args(self, n):
        self.A = np.asarray(np.random.rand(self.LARGEDIM, n), dtype=dtype)
        self.B = np.asarray(np.random.rand(n, self.LARGEDIM), dtype=dtype)
        self.C = np.asarray(np.random.rand(self.LARGEDIM, self.LARGEDIM), dtype=dtype)

    def compute(self):
        self.A.dot(self.B, out=self.C)

class cholesky(Bench):
    def ops(self, n):
        return n*n*n/3.0*1e-9

    def make_args(self, n):
        self.A = np.asarray(np.random.rand(n,n), dtype=dtype)
        self.A = np.asfortranarray(self.A*self.A.transpose() + n*np.eye(n))

    def compute(self):
        scipy.linalg.cholesky(self.A, lower=False, overwrite_a=True, check_finite=False)

class lu(Bench):
    def ops(self, n):
        return 2./3.*n*n*n*1e-9

    def make_args(self, n):
        self.A = np.asfortranarray(np.asarray(np.random.rand(n,n), dtype=dtype))

    def compute(self):
        scipy.linalg.lu(a=self.A, overwrite_a=True, check_finite=False)

class inv(Bench):
    def ops(self, n):
        # scipy is getrf getri
        return 2.*n*n*n*1e-9
        # numpy calls gesv
        # lu + triangular solve
        # TRF + TRS
        # 2/3 n^3 + 2 n^3 = 8/3 n^3
        # return 8./3.*N*N*N*1e-9

    def make_args(self, n):
        self.A = np.asfortranarray(np.random.rand(n,n), dtype=dtype)

    def compute(self):
        scipy.linalg.inv(self.A, overwrite_a=True, check_finite=False)

class det(Bench):
    def ops(self, n):
        return 2./3.*n*n*n*1e-9

    def make_args(self, n):
        self.A = np.asfortranarray(np.random.rand(n,n), dtype=dtype)

    def compute(self):
        scipy.linalg.det(self.A, overwrite_a=True, check_finite=False)

class fft(Bench):
    # If you change the value of runs, change native.cpp as well
    runs = 1000

    def ops(self, n):
        # This is not an actual flop count; it is simply a convenient scaling,
        # based on the fact that the radix-2 Cooley-Tukey algorithm asymptotically
        # requires 5 N log2(N) floating-point operations.
        # http://www.fftw.org/speed/method.html
        return self.runs*5*n*math.log(n,2)*1e-9

    def make_args(self, n):
        self.A = np.asarray(np.random.rand(n), dtype=np.complex128)

    def compute(self):
        for i in range(self.runs):
            scipy.fftpack.fft(self.A, overwrite_x = True)

def capture_multiline_output(command):
    try:
        return str(subprocess.check_output(command,shell=True)).split('\\n')
    except:
        return ''

def set_from_environ(results, key):
    results[key] = os.environ[key] if key in os.environ else 'not set'

def add_configuration():
    time = datetime.datetime.now()
    results['name'] = args.name
    results['date'] = time.strftime('%Y-%m-%d-%H-%M-%S')
    set_from_environ(results,'KMP_AFFINITY')
    set_from_environ(results,'OMP_NUM_THREADS')
    set_from_environ(results,'MKL_NUM_THREADS')
    results['host'] = platform.node()
    results['lscpu'] = capture_multiline_output('lscpu')
    results['numactl'] = capture_multiline_output('numactl --show')
    results['pip list'] = capture_multiline_output('/usr/bin/pip list')
    results['conda'] = capture_multiline_output('conda list')
    results['runs'] = []

def write_output():
    try:
        os.mkdir('runs')
    except:
        pass
    filename = 'bench-%s.json' % results['date']
    path = 'runs/%s' % filename
    with open(path, 'w') as out:
        json.dump(results,out,indent=2)
    if os.path.exists('runs/last.json'):
        os.remove('runs/last.json')
    os.symlink(filename,'runs/last.json')
    

def this_dir(file):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),file)

def parse_bench(bench_strings):
    benches = []
    for bs in bench_strings:
        b = bs.split(':')
        benches.append((b[0],8 if len(bs) == 1 else int(b[1])))
    return benches

def parse_args():
    default_bench = ['dot:8']
    parser = argparse.ArgumentParser("Benchmark runner.")
    parser.add_argument('--name', help="Name of run for log file")
    parser.add_argument('--bench', default=None, nargs='+', help="Benchmark to run. Default %s" % default_bench)
    parser.add_argument('--runs', default=3, type=int, help="Number of runs")
    parser.add_argument('-q', default=False, action='store_true', help="Logging")
    args = parser.parse_args()
    benchmarks = parse_bench(args.bench if args.bench else default_bench)
    return (args,benchmarks)

if __name__ == '__main__':
    (args,benchmarks) = parse_args()
    add_configuration()
        
    for (bench_name,n) in benchmarks:
        bench = globals()[bench_name]()
        bench.measure(n, args.runs)
        del bench

    write_output()
