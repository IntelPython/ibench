import argparse
import os
import sys

from .cmds import run
from .cmds import configs

cmds = [run, configs]

def parse_args():
    parser = argparse.ArgumentParser("ibench")
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers()
    for cmd in cmds:
        cmd.add_parser(subparsers)
    return parser.parse_args()

# Load plugins first so it can modify everything that follows
if 'IBENCH_PLUGINS' in os.environ:
    for plugin in os.environ['IBENCH_PLUGINS'].split(' '):
        __import__(plugin)

args = parse_args()
if args.func:
    args.func(args)
