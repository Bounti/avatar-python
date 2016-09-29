#!/usr/bin/python3

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from avatar.tests.test_configuration import *
from avatar.tests.test_analyzer import *
from avatar.tests.test_target import *
from avatar.tests.test_emulator import *

if __name__ == "__main__" :
    exit_code = test()
    if not exit_code is None:
        sys.exit(exit_code)
