'''
@author: Luca BRUNO <lucab@debian.org>
@author: Nassim Corteggiani <nassim.corteggiani@maximintegrated.com>

'''
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
from avatar.targets.openocd.jig import Jig
from avatar.system import *

import sys

import socket
import subprocess
import logging
import time
import os

log = logging.getLogger(__name__)

class OpenocdJig(Jig):

    def __init__(self, fname, exec_path, base_dir, options="", debug=False):

        self._fname = fname
        self._exec_path = exec_path
        self._base_dir = base_dir
        self._options = options
        self._debug = debug

        self._openocd_pid = None

        self._log = None

    def attach(self):
        try:
            with open(self._base_dir+"/openocd_std.log", "w+") as self._log:
                self._openocd_pid = subprocess.Popen([self._exec_path, "-f", self._fname, self._options],\
                        stdout = self._log,
                        stderr = self._log)
        except FileNotFoundError as e:
            raise FileNotFoundError("Unable to find openocd : %s" % self._exec_path)

    def detach(self):
        if self._log is not None and self._openocd_pid is not None :
            self._openocd_pid.kill()
            self._log.close()

    def __del__(self):
        self.detach()
