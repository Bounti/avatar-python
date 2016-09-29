from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
from avatar.emulators.emulator import Emulator

class KleeEmulator(Emulator):

    def __init__(self, binary, exec_path, base_dir, options="", debug=False):

        self._binary = binary
        self._exec_path = exec_path
        self._base_dir = base_dir
        self._options = options
        self._debug = debug

        self._log = None

        self._name = "Klee"
        self._process = None

    def __str__(self):
        return self._name

    def init(self):
        pass

    def start(self):
        try:
            with open(self._base_dir+"/klee_std.log", "w+") as self._log:
                self._process = subprocess.Popen([self._exec_path, self._options, self._binary],\
                        stdout = self._log,
                        stderr = self._log)
        except FileNotFoundError as e:
            raise FileNotFoundError("Unable to find openocd : %s" % self._exec_path)

    def stop(self):
        if self._log is not None and self._openocd_pid is not None :
            self._process.kill()
            self._log.close()

