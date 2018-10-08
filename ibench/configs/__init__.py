# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: MIT

from . import conda_py2
from . import direct
from . import idp201700
from . import idp201701
from . import pip

configs = {
    'conda_py2': conda_py2.Conda_py2,
    'direct': direct.Direct,
    'idp201700': idp201700.IDP201700,
    'idp201701': idp201701.IDP201701,
    'pip': pip.Pip,
}
