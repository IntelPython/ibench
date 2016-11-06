import subprocess

def test_basic():
    subprocess.check_call('python -m ibench configs --threads 1 --cpu xeon --run direct --run_args -b cholesky fft det inv lu svd qr dot --quick --file foo', shell=True)
