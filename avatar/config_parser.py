from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
from builtins import object
import pickle

class ConfigParser(object):

    def __init__(self, path_to_config):
        self._data = []

        self._path = path_to_config

        self._parse_analyzer_configuration()

        self._parse_target_configuration()

        self._parse_emulator_configuration()

        self._data = ""

        with open(self._path, 'r') as f:
            self._data = f.read()

        self._source = pickle.loads(self._data)

    def _parse_analyzer_configuration(self):
        assert ("analyzer" in self._data), \
            "Analyzer configuration missing"
        self._analyzer_config = self._data["analyzer"]

        keys = ["verbose","exec_path","gdb_path","gdb_options","klee_options","plugins"]

        config = self.parse_config(keys, self._emulator_config)

        self.__setitem__("analyzer", config)

    def _parse_target_configuration(self):
        assert ("target" in self._data), \
            "Target configuration missing"
        self._target_config = self._data["target"]

        keys = ["config_file","protocol","port","host","exec_path","options","log_stdout"]

        config = self.parse_config(keys, self._emulator_config)

        self.__setitem__("target", config)

    def _parse_emulator_configuration(self):
        assert ("emulator" in self._data), \
            "Emulator configuration missing"
        self._emulator_config = self._data["emulator"]

        keys = ["qemu_configuration","machine_configuration","avatar_configuration"]

        config = self.parse_config(keys, self._emulator_config)

        self.__setitem__("emulator", config)

    def __setitem__(self, key, item):
        self._data[key] = item

    def __getitem__(self, key):
        return self._data[key]

    def parse_config(self, expected_config, source):
        assert (isinstance(expected_config, list)), \
            "Expected configuration must be a list"

        out = {}

        for key in expected_config:
            assert (key in source), \
                "Bad user settings : unable to locate '%s' setting" % key
            out[key] = self._symbolic_engine_settings[key]

        return out
