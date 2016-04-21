'''
@author: Luca BRUNO <lucab@debian.org>
'''
from avatar.targets.openocd.jig import Jig

import sys

import socket
import logging
import subprocess
import time
import os

log = logging.getLogger(__name__)

class OpenocdJig(Jig):

    def __init__(self, fname):

        self.__fname = fname

    def attach(self):
        with open(os.devnull, "w") as fnull:
            self._pid = subprocess.Popen(["openocd", "-f", self.__fname], stdout=fnull, stderr=fnull)
        time.sleep(1)

    def detach(self):
        self._pid.kill()

    def __del__(self):
        self.detach()
