#  maps from string name to callable
config_map = {}
benchmark_map = {}
cmd_map = {}

# import the packages so they register with the maps above
import ibench.configs
import ibench.cmds
import ibench.benchmarks
