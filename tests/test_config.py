# Copyright (C) 2016-2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

import subprocess

def test_auto_size():
    subprocess.check_call('python -m ibench configs --build pip', shell=True)
    subprocess.check_call('python -m ibench configs --size auto --cpu xeon --run idp201700 --run-args "-b dot"', shell=True)

def test_py2():
    # only run if conda is present
    ret = subprocess.call('which conda',shell=True)
    if ret == 0:
        subprocess.check_call('python -m ibench configs --build conda_py2', shell=True)

def test_direct():
    subprocess.check_call('python -m ibench configs --threads 1 --cpu xeon --run direct --run-args "-b cholesky fft det inv lu svd qr dot --size test"', shell=True)

def test_docker_build():
    subprocess.check_call('python -m ibench configs --build pip', shell=True)

def test_pip():
    subprocess.check_call('python -m ibench configs --build pip', shell=True)
    subprocess.check_call('python -m ibench configs --threads 1 --cpu xeon --run pip --run-args "-b det --size test"', shell=True)

def test_idp():
    subprocess.check_call('python -m ibench configs --build pip', shell=True)
    subprocess.check_call('python -m ibench configs --threads 1 --cpu xeon --run idp201700 idp201701 --run-args "-b det --size test"', shell=True)

