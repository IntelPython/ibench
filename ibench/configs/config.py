from __future__ import print_function
import os
import subprocess
import sys

class Config:
    _docker = None
    _python_path = '/usr/bin/python'
    _affinity = None
    _numactl = None

    def __init__(self, cmd):
        self.name = self.__class__.__name__
        self._cmd = cmd
        if self._cmd.args.cpu == 'xeon':
            self._affinity = 'compact'
            self._numactl = '--interleave=all'

    def _add_docker_env(self, key, value):
        if self._docker:
            c = ' -e'
        else:
            c = ''
        c += ' %s=%s' % (key,value)
        return c

    def _log(self, message):
        if self._cmd.args.quiet:
            return
        print('%s: %s' % (self.name,message), file=sys.stderr)

    def build(self):
        pass

    def run(self, threads):
        cmd = ''
        if self._docker:
            cmd += 'docker run'
            if self._cmd.args.editable:
                cmd += ' -v %s:/ibench-master' % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if threads > 0:
            cmd += self._add_docker_env('OMP_NUM_THREADS', threads)
        if self._affinity:
            cmd += self._add_docker_env('KMP_AFFINITY', self._affinity)
        if self._docker:
            cmd += ' --rm -it %s' % self._docker
        if self._numactl:
            cmd += ' numactl %s' % self._numactl
        cmd += ' %s' % self._python_path
        cmd += ' -m ibench run'
        if len(self._cmd.run_args) > 0:
            cmd += '  %s' % ' '.join(self._cmd.run_args)
        self._log(cmd)
        if not self._cmd.args.dry_run:
            subprocess.check_output(cmd,shell=True)
