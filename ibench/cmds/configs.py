import argparse


from .cmd import Cmd
from ..configs import configs


def add_parser(subparsers):
    parser = subparsers.add_parser('configs')
    parser.set_defaults(func=Configs)
    parser.add_argument('--run-args',
                        default='',
                        help='arguments to pass to run command')
    parser.add_argument('--cpu', 
                        choices=['xeon','phi','core'],
                        default='xeon',
                        help='cpu executing the benchmarks')
    parser.add_argument('--dry-run', 
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
                        choices=['auto','small','large','tiny','test'],
                        help='Size of problem. auto adjusts size so test will finish in a few minutes')
    parser.add_argument('--threads', 
                        default=None, 
                        nargs='+', 
                        type=int, 
                        help="Number of threads to use")

class Configs(Cmd):

    def __init__(self, args):
        if args.threads:
            self._threads = args.threads
        elif args.cpu == 'xeon':
            self._threads = [1,32]
        elif args.cpu == 'phi':
            self._threads = [1,64]
        elif args.cpu == 'core':
            self._threads = [1,2]

        for config_name in args.build:
            config = configs[config_name](args)
            config.build()
        for config_name in args.run:
            config = configs[config_name](args)
            for threads in self._threads:
                config.run(threads)
