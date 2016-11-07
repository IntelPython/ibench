import argparse
import datetime
import json
import os
import platform
import subprocess
import sys
import time

from ibench.benchmarks.cholesky import Cholesky
from ibench.benchmarks.det import Det
from ibench.benchmarks.dot import Dot
from ibench.benchmarks.fft import FFT
from ibench.benchmarks.inv import Inv
from ibench.benchmarks.lu import LU
from ibench.benchmarks.qr import QR
from ibench.benchmarks.svd import SVD

from ibench.cmds.cmd import Cmd

benchmarks = {
    'cholesky': Cholesky,
    'det': Det,
    'dot': Dot,
    'fft': FFT,
    'inv': Inv,
    'lu': LU,
    'qr': QR,
    'svd': SVD
}

benchmark_groups = {
    'linalg': ['cholesky', 'det', 'dot', 'inv', 'lu', 'qr', 'svd'],
    'all': list(benchmarks.keys())
}

def capture_multiline_output(command):
    try:
        return str(subprocess.check_output(command,shell=True)).split('\\n')
    except:
        return ''


class Run(Cmd):
    results = {}

    def __init__(self, arglist):
        '''Run a set of benchmarks'''
        self._parse_args(arglist)
        self._add_configuration()
        for bench_name in self._bmarks:
            bench = benchmarks[bench_name](self)
            if bench_name in self._sizes:
                n = self._sizes[bench_name]
            else:
                n = bench.size
            bench.measure(n)
            del bench
        self._write_output()

    def _parse_bench(self,default_bench):
        self._bmarks = []
        self._sizes = {}
        for bs in self.args.benchmarks if self.args.benchmarks else default_bench:
            b = bs.split(':')
            blist = list(benchmarks.keys()) + list(benchmark_groups.keys())
            if b[0] not in blist:
                self._cmd_error('Unknown benchmark: %s. Choices are: %s' % (b[0],','.join(blist)))
            # process arguments for a size
            if len(b) == 1:
                if self.args.quick:
                    size = 2
            elif len(b) == 2:
                size = int(b[1])
            else:
                self._cmd_error('invalid benchmark spec: %s' % bs)

            # expand groups
            group = benchmark_groups[b[0]] if b[0] in benchmark_groups else [b[0]]
            self._bmarks.extend(group)
            for bench in group:
                self._sizes[bench] = size

    def _parse_args(self, arglist):
        default_bench = ['dot']
        parser = argparse.ArgumentParser('ibench')
        parser.add_argument('-b','--benchmarks', 
                            default=None, 
                            nargs='+', 
                            help='Benchmark to run. Default %s' % default_bench)
        parser.add_argument('--file', 
                            help='Write results to <file> instead of stdout')
        parser.add_argument('--name', 
                            default='noname', 
                            help='Descriptive name of run to include in results file')
        parser.add_argument('--quick', 
                            default=False, 
                            action='store_true', 
                            help="Quick run by using small sizes")
        parser.add_argument('-q', 
                            '--quiet', 
                            default=False, 
                            action='store_true', 
                            help="Logging")
        parser.add_argument('--runs', default=3, type=int, help='Number of runs')
        self.args = parser.parse_args(arglist)
        self._parse_bench(default_bench)
        
    def _set_from_environ(self, key):
        self.results[key] = os.environ[key] if key in os.environ else 'not set'

    def _add_configuration(self):
        results = self.results
        time = datetime.datetime.now()
        results['name'] = self.args.name
        results['date'] = time.strftime('%Y-%m-%d-%H-%M-%S')
        self._set_from_environ('KMP_AFFINITY')
        self._set_from_environ('OMP_NUM_THREADS')
        self._set_from_environ('MKL_NUM_THREADS')
        results['host'] = platform.node()
        results['lscpu'] = capture_multiline_output('lscpu')
        results['numactl'] = capture_multiline_output('numactl --show')
        results['pip list'] = capture_multiline_output('/usr/bin/pip list')
        results['conda'] = capture_multiline_output('conda list')
        results['runs'] = []

    def _write_output(self):
        filename = self.args.file
        fh = open(filename, 'w') if filename else sys.stdout
        json.dump(self.results,fh,indent=2)
        if filename:
            fh.close()
