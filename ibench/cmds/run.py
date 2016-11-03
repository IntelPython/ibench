import argparse
import datetime
import json
import os
import platform
import subprocess
import sys
import time

import ibench
from ibench.cmds.cmd import Cmd

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
            bench = ibench.benchmark_map[bench_name](self)
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
            if b[0] not in ibench.benchmark_map.keys():
                self._cmd_error('Unknown benchmark: %s. Choices are: %s' % (b[0],','.join(ibench.benchmark_map.keys())))
            self._bmarks.append(b[0])
            # process arguments for a size
            if len(b) == 1:
                if self.args.quick:
                    self._sizes[b[0]] = 8
            elif len(b) == 2:
                self._sizes[b[0]] = int(b[1])
            else:
                self._cmd_error('invalid benchmark spec: %s' % bs)

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

ibench.cmd_map['run'] = globals()['Run']
