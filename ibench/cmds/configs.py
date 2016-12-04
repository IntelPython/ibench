import argparse


from .cmd import Cmd
from ..configs import configs


class Configs(Cmd):

    def __init__(self, arglist):
        self._parse_args(arglist)
        for config_name in self.args.build:
            config = configs[config_name](self)
            config.build()
        for config_name in self.args.run:
            config = configs[config_name](self)
            for threads in self._threads:
                config.run(threads)

    def _parse_args(self,arglist):
        parser = argparse.ArgumentParser('ibench configs')
        parser.add_argument('--cpu', 
                            choices=['xeon','phi'],
                            default='xeon',
                            help='cpu executing the benchmarks')
        parser.add_argument('--dry_run', 
                            default=False, 
                            action='store_true', 
                            help="Emit commands, but do not run them")
        parser.add_argument('--editable', 
                            default=True, 
                            action='store_true', 
                            help="Install ibench editable in docker image so we can change it")
        parser.add_argument('-q', 
                            '--quiet', 
                            default=False, 
                            action='store_true', 
                            help="Logging")
        parser.add_argument('--build', 
                            default=[], 
                            choices=configs.keys(),
                            nargs='+', 
                            help='Configs to build')
        parser.add_argument('--run', 
                            default=[], 
                            choices=configs.keys(),
                            nargs='+', 
                            help='Configs to run')
        parser.add_argument('--size', 
                            default='test',
                            choices=['auto','small','large','test'],
                            help='Size of problem. auto adjusts size so test will finish in a few minutes')
        parser.add_argument('--threads', 
                            default=None, 
                            type=int, 
                            help="Number of threads to use")

        config_args = arglist
        self.run_args = []
        for i in range(len(arglist)):
            if arglist[i] == '--run_args':
                config_args = arglist[:i]
                self.run_args = arglist[i+1:]

        self.args = parser.parse_args(config_args)

        if self.args.threads:
            self._threads = [self.args.threads]
        elif self.args.cpu == 'xeon':
            self._threads = [1,32]
        elif self.args.cpu == 'phi':
            self._threads = [1,64]
