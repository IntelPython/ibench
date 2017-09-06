# ibench

Benchmarks for Intel Distribution for Python

## Install
        # Since you want to benchmark numpy/scipy, manually install the one you want
        # instead of letting pip install one
        # cython is needed to build native extensions in ibench_native
        conda install scipy cython
        pip install -e .

## Run
        # basic command
        python -m ibench run -p all --size large --runs 3 --file all.out
        # Use ibench_native plugin to include native versions of the benchmarks. See the ibench_native repository
        IBENCH_PUGINS=ibench_native python -m ibench run -p dot_native --size large --runs 3 --file all.out

## Help
        python -m ibench --help
        python -m ibench run --help
