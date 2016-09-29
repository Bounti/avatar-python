from avatar.emulators.emulator import Emulator
import subprocess
import logging

log = logging.getLogger(__name__)

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
                self._process = subprocess.Popen([self._exec_path, self._binary],\
                    stdout = self._log,
                    stderr = self._log)
        except FileNotFoundError as e:
            raise FileNotFoundError("Unable to find Klee : %s" % self._exec_path)

    def stop(self):
        if self._log is not None and self._process is not None :
            self._process.kill()
            self._log.close()
