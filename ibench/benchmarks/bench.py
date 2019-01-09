# Copyright (C) 2016-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import print_function
import gc
import numpy as np
import sys
import time

class Bench:
    _dtype = np.double

    def __init__(self, cmd):
        self.name = self.__class__.__name__
        self._cmd = cmd

    def _log(self, message):
        if self._cmd.args.quiet:
            return
        print('%s: %s' % (self.name,message), file=sys.stderr)

    def _run(self, n):
        self._make_args(n)

        # Disable garbage collector
        gcold = gc.isenabled()
        gc.disable()

        times = []
        for i in range(self._cmd.args.runs):
            t_start = time.time()
            self._compute()
            elapsed = time.time() - t_start
            times.append(elapsed)

        if gcold:
            gc.enable()

        return times

    def measure(self, n, args):
        self._log('')
        self._log('  N = %d' % n)

        times = self._run(n)

        ops = self._ops(n)
        if args.gflops is False:
            for elapsed in times:
                self._log('  elapsed %f' % (elapsed))

        else:
            for elapsed in times:
                self._log('  elapsed %f gflops %f' % (elapsed,ops/elapsed))

        self._summarize(n, times, args)

    def _summarize(self, n, times, args):
        t = np.asarray(times)
        median = np.median(t)
        ops = self._ops(n)
        if args.gflops is False:
            self._cmd.results['runs'].append({'name': self.name,
                                              'N': n,
                                              'times': times,
                                              'stats': {'min': np.amin(t),
                                                        'max': np.max(t),
                                                        'median': median}})
        else:
            self._log('  gflops %f' % (ops/median))
            self._cmd.results['runs'].append({'name': self.name,
                                              'N': n,
                                              'gflops': ops/median,
                                              'ops': ops,
                                              'times': times,
                                              'stats': {'min': np.amin(t),
                                                        'max': np.max(t),
                                                        'median': median}})
