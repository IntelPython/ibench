from __future__ import print_function
import datetime
import os
import subprocess
import sys

class Config:
    _docker = None
    _python_path = '/usr/bin/python'
    _affinity = None
    _numactl = None
    _mt_size = 'large'
    _st_size = 'small'

    def __init__(self, args):
        self.name = self.__class__.__name__
        self.args = args
        if self.args.cpu == 'xeon':
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
        if self.args.quiet:
            return
        print('%s: %s' % (self.name,message), file=sys.stderr)

    def build(self):
        pass

    def size(self, threads):
        if self.args.size != 'auto':
            return self.args.size
        return self._mt_size if threads > 1 else self._st_size

    def run(self, threads):
        cmd = ''
        if self._docker:
            cmd += 'docker run'
            if self.args.editable:
                cmd += ' -v %s:/ibench-master' % os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if threads > 0:
            cmd += self._add_docker_env('OMP_NUM_THREADS', threads)
        if self._affinity:
            cmd += self._add_docker_env('KMP_AFFINITY', self._affinity)
        if self._docker:
            cmd += ' --rm %s' % self._docker
        if self._numactl:
            cmd += ' numactl %s' % self._numactl
        cmd += ' %s' % self._python_path
        cmd += ' -m ibench run'
        cmd += ' --name %s' % self.name
        cmd += ' --size %s' % self.size(threads)
        cmd += '  %s' % self.args.run_args
        self._log(cmd)
        if not self.args.dry_run:
            time = datetime.datetime.now()
            date = time.strftime('%Y-%m-%d-%H-%M-%S')
            try:
                os.mkdir('results')
            except OSError:
                pass
            filename = 'results/bench-%s.json' % date
            with open(filename,'w') as stdoutfp:
                subprocess.call(cmd,stdout=stdoutfp,shell=True)
