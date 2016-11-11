import argparse
import sys

from ibench.cmds import cmds

def parse_bench(bench_strings):
    '''Change from list of bench:n to list of (bench,n)'''
    benches = []
    for bs in bench_strings:
        b = bs.split(':')
        benches.append((b[0],8 if len(bs) == 1 else int(b[1])))
    return benches

def parse_args():
    parser = argparse.ArgumentParser("ibench")
    parser.add_argument('cmd', 
                        choices=cmds.keys(),
                        help='cmd to execute')
    return parser.parse_args(sys.argv[1:2])


args = parse_args()
cmds[args.cmd](sys.argv[2:])
