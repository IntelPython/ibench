# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: MIT

import subprocess

subprocess.run('python -m pytest tests', shell=True, check=True)
