# set up script on NERSC Cori machine 
module load python/3.5-anaconda
if [[ ! -d $HOME/.conda ]]; then
  mkdir $HOME/.conda
fi

conda create -n wrapped_ibench -c intel -c intel/label/hugetlbfs -y python=3.6 hugetlbfs scipy
source $HOME/.conda/envs/ibench/bin/activate wrapped_ibench
cd ../../
python setup.py install
