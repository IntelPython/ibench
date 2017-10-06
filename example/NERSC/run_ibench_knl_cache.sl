#!/bin/bash -l

#SBATCH -N 1               
#SBATCH -p regular
#SBATCH -t 00:45:00
#SBATCH -C knl,quad,cache

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

module load python/3.5-anaconda
source $HOME/.conda/envs/wrapped_ibench/bin/activate wrapped_ibench

# Make sure that the transparent huge page is enabled for best performance  
module load craype-hugepages2M

#### This is a script for running the benchmark
srun -N 1 python -m ibench run -b $TEST --size $SIZE --file \
$OUTPUT_DIR/${TEST}_${SIZE}_$(date '+%Y-%m-%d_%H:%M:%S').log
