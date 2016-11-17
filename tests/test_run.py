import subprocess

def test_run_plugin():
    subprocess.check_call('python -m ibench run -p os sys -b cholesky --quick --file foo', shell=True)

def test_run():
    subprocess.check_call('python -m ibench run', shell=True)

def test_run_simple():
    subprocess.check_call('python -m ibench run -b cholesky --quick --file foo', shell=True)

def test_run_sizes():
    subprocess.check_call('python -m ibench run -b cholesky:3 --quick --file foo', shell=True)

def test_run_groups():
    subprocess.check_call('python -m ibench run -b linalg --quick --file foo', shell=True)
