#!/usr/bin/python3

from avatar.tests.test_configuration import *
from avatar.tests.test_analyzer import *
from avatar.tests.test_target import *
from avatar.tests.test_emulator import *

if __name__ == "__main__" :
    exit_code = test()
    if not exit_code is None:
        sys.exit(exit_code)
