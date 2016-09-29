from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import os

from avatar.configuration.parser.parser import Parser

class ParserV1(Parser):

    #TODO : use call to create dynamical attribut from fields list
    def getOutputDirectory(self):
        return self._output_directory

    def __getOutputError(category, field):
        return "Bad user settings : Unable to locate %s '%s' settings" \
            % (category, field)

    def __init__(self, user_settings):
        assert (isinstance(user_settings, dict)), \
            "User settings must be a dictionary"
        self._settings = user_settings

        assert (self._settings["output_directory"]), \
            "Bad user settings : Unable to locate 'output_directory' settings"
        self._output_directory = self._settings["output_directory"]

    def checkOpenocdTargetConfiguration(self):

        assert ("avatar_configuration" in self._settings), \
            "Bad user settings : Unable to locate openocd target 'avatar_configuration' settings"
        avatar_settings_details = self._target_settings["avatar_configuration"]

        assert ("target_gdb_address" in avatar_settings_details), \
            "Bad user settings : Unable to locate openocd target 'target_gdb_address' setting"
        address = avatar_settings_details["target_gdb_address"]

        assert ("target_gdb_path" in avatar_settings_details), \
            "Bad user settings : Unable to locate openocd target 'target_gdb_path' setting"
        gdb_path = avatar_settings_details["target_gdb_path"]

        assert ("openocd_configuration" in self._settings), \
            "Bad user settings : Unable to locate openocd target 'openocd_configuration' settings"
        openocd_settings_details = self._target_settings["openocd_configuration"]

        assert ("config_file" in openocd_settings_details), \
            "Bad user settings : Unable to locate openocd target 'config_file' setting"
        config_file = openocd_settings_details["config_file"]

        if config_file[0] != '/':
            config_file = self._directory_settings + '/' + config_file

        index1 = str.find(':')
        index2= str.find(':')

        protocol = str[0:index1]
        host = str[index1+1:index2]
        port = str[index2+1:]

        return {"config_file"   : config_file,
                "host"          : host,
                "protocol"      : protocol,
                "port"          : port,
                "exec_path"     : exec_path,
                "options"       : options,
                "log_stdout"    : log_stdout,
                "base_dir"      : self._directory_settings}

    def checkGlobalTargetConfiguration(self):

        assert (self._settings["avatar_configuration"]), "Bad user settings : Unable to locate avatar_configuration settings"

        return {"name":"gdb", "configuration": self._settings["avatar_configuration"]}


    def checkGlobalAnalyzerConfiguration(self):

        assert (self._settings["s2e"]), "Bad user settings : Unable to locate S2E settings"

        return {"name":"s2e", "configuration": self._settings["s2e"]}

    def checkGlobalEmulatorConfiguration(self):

        assert (self._settings["qemu_configuration"]), "Bad user settings : Unable to locate qemu_configuration settings"

        assert (self._settings["machine_configuration"]), "Bad user settings : Unable to locate machine_configuration settings"

        assert (self._settings["avatar_configuration"]), "Bad user settings : Unable to locate avatar_configuration settings"

        qemu_configuration = {
            "qemu_configuration"        : self._settings["qemu_configuration"],
            "machine_configuration"     : self._settings["machine_configuration"],
            "avatar_configuration"      : self._settings["avatar_configuration"],
        }

        return {"name":"qemu", "configuration": self._settings["qemu_configuration"]}

    def checkQEmuEmulatorConfiguration(self):

        assert (self._settings["qemu_configuration"]), "Bad user settings : Unable to locate qemu_configuration settings"

        assert (self._settings["machine_configuration"]), "Bad user settings : Unable to locate machine_configuration settings"

        assert (self._settings["avatar_configuration"]), "Bad user settings : Unable to locate avatar_configuration settings"

        qemu_configuration = {
            "qemu_configuration"        : self._settings["qemu_configuration"],
            "machine_configuration"     : self._settings["machine_configuration"],
            "avatar_configuration"      : self._settings["avatar_configuration"],
        }

        return {"emulator"      : qemu_configuration,
                "base_dir"  : self._directory_settings,
                "output_dir" : self._output_directory}

    def checkKleeEmulatorConfiguration(self):

        raise NotImplementedError("Unimplmented Klee Analyzer")

    def checkS2EEmulatorConfiguration(self):

        keys = ["verbose","s2e_binary","gdb_path","gdb_options","klee_options","plugins"]
        s2e_values = self.checkConfiguration(keys, self._analyzer_settings)
