import subprocess

def test_py2():
    subprocess.check_call('python -m ibench configs --build conda_py2', shell=True)

def test_direct():
    subprocess.check_call('python -m ibench configs --threads 1 --cpu xeon --run direct --run_args -b cholesky fft det inv lu svd qr dot --quick --file foo', shell=True)

def test_docker_build():
    subprocess.check_call('python -m ibench configs --build pip', shell=True)

def test_pip():
    subprocess.check_call('python -m ibench configs --threads 1 --cpu xeon --run pip --run_args -b det --quick --file foo', shell=True)
