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

## Running benchmarks by domain

### Linear algebra
- To run python benchmarks: `python -m ibench run -b linalg --size large --runs 3 --file linalg.out`
- To run native benchmarks*: `python -m ibench run -b native --size large --runs 3 --file native.out`

\* Currently, native benchmarks are only available for `det`, `dot`, `lu`, and `inv`.

### scikit-learn
- To run python benchmarks: `python -m ibench run -b sklearn --size large --runs 3 --file sklearn.out`

### Others
- To run python FFT benchmark: `python -m ibench run -b fft --size large --runs 3 --file fft.out`
- To run python RNG benchmark: `python -m ibench run -b rng --size large --runs 3 --file rng.out`
- To run python Black-Scholes benchmark: `python -m ibench run -b blacksch --size large --runs 3 --file blacksch.out`


## Help
```bash
python -m ibench --help
python -m ibench run --help
```
