#!/bin/bash -l

# Copyright (C) 2016-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

#SBATCH -N 1               
#SBATCH -p regular
#SBATCH -t 00:45:00
#SBATCH -C knl,quad,cache

# specify threading settings
export KMP_AFFINITY=granularity=fine,compact
export NUM_OF_THREADS=$(grep 'model name' /proc/cpuinfo | wc -l)
export OMP_NUM_THREADS=$(( $NUM_OF_THREADS / 4  ))
export MKL_NUM_THREADS=$(( $NUM_OF_THREADS / 4  ))
export KMP_HW_SUBSET=${OMP_NUM_THREADS}c,1t  
export HPL_LARGEPAGE=1
export KMP_BLOCKTIME=800
export TEST=all
export SIZE=large
export OUTPUT_DIR="."

# load the python module on Cori
module load python/3.5-anaconda

# activate the relevant Conda environment
source $HOME/.conda/envs/wrapped_ibench/bin/activate wrapped_ibench

# make sure that the Cray transparent huge page module is loaded for the best performance  
module load craype-hugepages2M

# run the benchmark and specify the location and name of the log file
srun -N 1 python -m ibench run -b $TEST --size $SIZE --file \
$OUTPUT_DIR/${TEST}_${SIZE}_$(date '+%Y-%m-%d_%H:%M:%S').log
