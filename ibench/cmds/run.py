import argparse
import datetime
import json
import os
import platform
import subprocess
import sys
import time

from ..benchmarks import benchmarks
from ..benchmarks import benchmark_groups
from .cmd import Cmd

def capture_multiline_output(command):
    try:
        return str(subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)).split('\\n')
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
            n = bench.sizes[self.args.size]
            bench.measure(n)
            del bench
        self._write_output()

    def _load_plugins(self):
        '''Load plugins by importing, they self-register'''
        for plugin in self.args.plugins:
            __import__(plugin)

    def _parse_bench(self,default_bench):
        self._bmarks = []
        bstack = self.args.benchmarks if self.args.benchmarks else default_bench
        for bs in bstack:
            # expand groups
            if bs in benchmark_groups:
                bstack.extend(benchmark_groups[bs])
            elif bs in benchmarks:
                self._bmarks.append(bs)
            else:
                print('Unknown benchmark: ',
                      bs,
                      ' must be in: ',
                      list(benchmarks.keys()) + list(benchmark_groups.keys()),
                      file=sys.stderr)
                sys.exit(1)

    def _parse_args(self, arglist):
        default_bench = ['dot']
        parser = argparse.ArgumentParser('ibench run')
        parser.add_argument('-b','--benchmarks', 
                            nargs='+', 
                            help='Benchmarks to run')
        parser.add_argument('--file', 
                            help='Write results to <file> instead of stdout')
        parser.add_argument('--name', 
                            default='noname', 
                            help='Descriptive name of run to include in results file')
        parser.add_argument('-p','--plugins', 
                            default=[],
                            nargs='+', 
                            help='1 or more plugins')
        parser.add_argument('--size', 
                            choices=['large','small','test'],
                            default='test',
                            help='Size of workload to run. In general, use large for multicore, small for single thread, and test for debugging')
        parser.add_argument('-q', 
                            '--quiet', 
                            default=False, 
                            action='store_true', 
                            help="Logging")
        parser.add_argument('--runs', default=3, type=int, help='Number of runs')
        self.args = parser.parse_args(arglist)
        self._load_plugins()
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
