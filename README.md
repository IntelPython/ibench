# ibench

Benchmarks for Intel Distribution for Python

## Install
```bash
# Since you want to benchmark numpy/scipy, manually install the one you want
# instead of letting pip install one
# cython is needed to build native extensions in ibench_native
conda install scipy cython scikit-learn
pip install -v --upgrade .
```

### Native versions
If `icc` and `cython` are available during the build, they will be used
to build native benchmarks. To specify a different compiler, specify one
in the environment variable `CXX`.

## Run
```bash
# basic command
python -m ibench run -b all --size large --runs 3 --file all.out
```

### Specifying benchmarks
- To run one or multiple benchmarks, pass the `-b BENCHMARKS...` option.
  Benchmarks can be specified individually, or in predefined groups
  (e.g. `native` contains all native benchmarks)
- To specify the problem size, use the `--size` option. This selects
  from a list of predefined problem sizes.

## Help
```bash
python -m ibench --help
python -m ibench run --help
```
