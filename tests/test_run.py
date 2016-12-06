import subprocess

def test_run_plugin():
    subprocess.check_call('IBENCH_PLUGINS="os sys" python -m ibench run -b cholesky --size test --file foo', shell=True)

def test_run():
    subprocess.check_call('python -m ibench run', shell=True)

def test_run_simple():
    subprocess.check_call('python -m ibench run -b cholesky --size test --file foo', shell=True)

def test_run_sizes():
    subprocess.check_call('python -m ibench run -b fft --size test --file foo', shell=True)
    subprocess.check_call('python -m ibench run -b fft --size small --file foo', shell=True)
    subprocess.check_call('python -m ibench run -b fft --size large --file foo', shell=True)

def test_run_groups():
    subprocess.check_call('python -m ibench run -b linalg --size test --file foo', shell=True)
