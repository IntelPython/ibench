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

### Configuring output
ibench supports both JSON (default) and CSV output with collection of
environment information. When using CSV format, ibench will prefix each
line of environment information with a comment character (default `@`).
Use the following arguments to the `run` subparser to configure its output:
- `-f,--format FORMAT` - use the specified format (`json` or `csv`)
- `--no-get-env-info` - don't collect environment or machine info
- `--env-info-prefix` - prefix character to use before environment info

## Running benchmarks by domain

### Linear Algebra
- To run python benchmarks: `python -m ibench run -b linalg --size large --runs 3 --file linalg.out`
- To run native benchmarks*: `python -m ibench run -b native --size large --runs 3 --file native.out`

\* Currently, native benchmarks are only available for `det`, `dot`, `lu`, and `inv`.

### Machine Learning
- To run python benchmarks: `python -m ibench run -b sklearn --size large --runs 3 --file sklearn.out`
- For comparable python and native benchmarks, see [scikit-learn_bench](https://github.com/IntelPython/scikit-learn_bench).

### Fast Fourier Transforms
- To run python benchmarks: `python -m ibench run -b fft --size large --runs 3 --file fft.out`
- For comparable python and native benchmarks, see [fft_benchmark](https://github.com/IntelPython/fft_benchmark).

### Random Number Generation
- To run python benchmarks: `python -m ibench run -b rng --size large --runs 3 --file rng.out`
- For comparable python and native benchmarks, see [optimizations_bench](https://github.com/IntelPython/optimizations_bench#random-number-generation).

### Black-Scholes Formula
- To run python Black-Scholes benchmark: `python -m ibench run -b blacksch --size large --runs 3 --file blacksch.out`
- For comparable python and native benchmarks, see [BlackScholes_bench](https://github.com/IntelPython/BlackScholes_bench).

### UMath
- See [optimizations_bench](https://github.com/IntelPython/optimizations_bench#random-number-generation).

## Help
```bash
python -m ibench --help
python -m ibench run --help
```
