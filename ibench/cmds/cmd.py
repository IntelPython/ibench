# Copyright (C) 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

from __future__ import print_function
import sys

class Cmd:
    def execute():
        pass

    def parse_args():
        pass

    def _cmd_error(self,message):
        print('error: %s' % message, file=sys.stderr)
        sys.exit(1)


        
