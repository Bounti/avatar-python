import os

class Configuration:

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

        assert ("configuration_directory" in self._settings), \
            self._getOutputError("", "configuration_directory")
        self._directory_settings = self._settings["configuration_directory"]

        assert ("analyzer" in self._settings), \
            "Bad user settings : Unable to locate 'analyzer' settings"
        self._analyzer_settings = self._settings["analyzer"]

        assert ("emulator" in self._settings), \
            "Bad user settings : Unable to locate 'emulator' settings"
        self._emulator_settings = self._settings["emulator"]

        assert ("target" in self._settings), \
            "Bad user settings : Unable to locate 'target' settings"
        self._target_settings = self._settings["target"]

        assert ("configuration" in self._target_settings), \
            "Bad user settings : Unable to locate openocd target 'configuration' settings"
        self._target_settings_details = self._target_settings["configuration"]

        assert (self._settings["output_directory"]), \
            "Bad user settings : Unable to locate 'output_directory' settings"
        self._output_directory = self._settings["output_directory"]


    def checkTargetConfiguration(self):

        assert ("config_file" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'config_file' setting"
        config_file = self._target_settings_details["config_file"]

        assert ("host" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'host' setting"
        host = self._target_settings_details["host"]

        assert ("protocol" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'protocol' setting"
        protocol = self._target_settings_details["protocol"]

        assert ("port" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'port' setting"
        port = self._target_settings_details["port"]

        if config_file[0] != '/':
            config_file = self._directory_settings + '/' + config_file

        assert ("exec_path" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'exec_path' setting"
        exec_path = self._target_settings_details["exec_path"]

        assert ("options" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'options' setting"
        options = self._target_settings_details["options"]

        assert ("log_stdout" in self._target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'log_stdout' setting"
        log_stdout = self._target_settings_details["log_stdout"]

        return {"config_file"   : config_file,
                "host"          : host,
                "protocol"      : protocol,
                "port"          : port,
                "exec_path"     : exec_path,
                "options"       : options,
                "log_stdout"    : log_stdout,
                "base_dir"      : self._directory_settings}


    def checkGlobalTargetConfiguration(self):
        assert (self._target_settings["name"]), "Bad user settings : Unable to locate target 'name' setting"
        name = self._target_settings["name"]

        assert (self._target_settings["configuration"]), "Bad user settings : Unable to locate target 'configuration' setting"
        configuration = self._target_settings["configuration"]

        return {"name":name, "configuration": configuration}


    def checkGlobalEmulatorConfiguration(self):
        assert (self._emulator_settings["name"]), "Bad user settings : Unable to locate Emulator 'name' setting"
        name = self._emulator_settings["name"]

        assert (self._emulator_settings["configuration"]), "Bad user settings : Unable to locate Emulator 'configuration' settings"
        configuration = self._emulator_settings["configuration"]

        return {"name":name, "configuration": configuration}

    def checkEmulatorConfiguration(self):

        assert ("configuration" in self._analyzer_settings), \
            "Bad user settings : Unable to locate symbolic engine 'configuration' settings"
        s2e = self._analyzer_settings["configuration"]

        assert ("configuration" in self._emulator_settings), \
            "Bad user settings : Unable to locate emulator 'configuration' settings"
        qemu = self._emulator_settings["configuration"]

        keys = ["verbose","exec_path","gdb_path","gdb_options","klee_options","plugins"]
        s2e_values = self.checkConfiguration(keys, self._analyzer_settings)

        return {"s2e"   : s2e,
                "qemu"  : qemu,
                "settings_dir" : self._directory_settings,
                "output_dir"      : self._output_directory}

    def checkConfiguration(self, keys, source):
        out = {}

        for key in source:
            assert (key in self._analyzer_settings), \
                "Bad user settings : Unable to locate analyzer '%s' settings" % key
            out[key] = self._analyzer_settings[key]

        return out
