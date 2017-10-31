# set up script on NERSC Cori machine 
module load python/3.5-anaconda
if [[ ! -d $HOME/.conda ]]; then
  mkdir $HOME/.conda
fi

conda create -n wrapped_ibench -c intel -y python=3.6 hugetlbfs scipy
source $HOME/.conda/envs/wrapped_ibench/bin/activate wrapped_ibench
cd ../../
python setup.py install
