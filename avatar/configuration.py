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

        assert (self._settings["output_directory"]), \
            "Bad user settings : Unable to locate 'output_directory' settings"
        self._output_directory = self._settings["output_directory"]

    def checkSuperspeedJtagConfiguration(self):

        assert ("configuration" in self._target_settings), \
            "Bad user settings : Unable to locate openocd target 'configuration' settings"
        target_settings_details = self._target_settings["configuration"]

        assert ("access-port" in target_settings_details), \
            "Bad user settings : Unable to locate superspeed-jtag target 'protocol' setting"
        ap = target_settings_details["access-port"]

        assert ("options" in target_settings_details), \
            "Bad user settings : Unable to locate superspeed-jtag target 'options' setting"
        options = target_settings_details["options"]

        assert ("log_stdout" in target_settings_details), \
            "Bad user settings : Unable to locate superspeed-jtag target 'log_stdout' setting"
        log_stdout = target_settings_details["log_stdout"]

        return {"access-port"   : ap,
                "options"       : options,
                "log_stdout"    : log_stdout,
                "base_dir"      : self._directory_settings}

    def checkOpenocdTargetConfiguration(self):

        assert ("configuration" in self._target_settings), \
            "Bad user settings : Unable to locate openocd target 'configuration' settings"
        target_settings_details = self._target_settings["configuration"]

        assert ("config_file" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'config_file' setting"
        config_file = target_settings_details["config_file"]

        assert ("host" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'host' setting"
        host = target_settings_details["host"]

        assert ("protocol" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'protocol' setting"
        protocol = target_settings_details["protocol"]

        assert ("port" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'port' setting"
        port = target_settings_details["port"]

        if config_file[0] != '/':
            config_file = self._directory_settings + '/' + config_file

        assert ("exec_path" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'exec_path' setting"
        exec_path = target_settings_details["exec_path"]

        assert ("options" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'options' setting"
        options = target_settings_details["options"]

        assert ("log_stdout" in target_settings_details), \
            "Bad user settings : Unable to locate openocd target 'log_stdout' setting"
        log_stdout = target_settings_details["log_stdout"]

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

    def checkGlobalAnalyzerConfiguration(self):

        assert (self._analyzer_settings["name"]), "Bad user settings : Unable to locate Analyzer 'name' setting"
        name = self._analyzer_settings["name"]

        assert (self._emulator_settings["configuration"]), "Bad user settings : Unable to locate analyzer 'configuration' settings"
        configuration = self._analyzer_settings["configuration"]

        return {"name":name, "configuration": configuration}

    def checkGlobalEmulatorConfiguration(self):

        assert (self._emulator_settings["name"]), "Bad user settings : Unable to locate Emulator 'name' setting"
        name = self._emulator_settings["name"]

        assert (self._emulator_settings["configuration"]), "Bad user settings : Unable to locate Emulator 'configuration' settings"
        configuration = self._emulator_settings["configuration"]

        return {"name":name, "configuration": configuration}

    def checkQEmuEmulatorConfiguration(self):

        assert ("configuration" in self._emulator_settings), \
            "Bad user settings : Unable to locate emulator 'configuration' settings"
        emulator = self._emulator_settings["configuration"]

        return {"emulator"      : emulator,
                "base_dir"  : self._directory_settings,
                "output_dir" : self._output_directory}

    def checkKleeEmulatorConfiguration(self):

        assert ("configuration" in self._emulator_settings), \
            "Bad user settings : Unable to locate emulator 'configuration' settings"
        emulator = self._emulator_settings["configuration"]

        return {"emulator"      : emulator,
                "base_dir"  : self._directory_settings,
                "output_dir" : self._output_directory}


    def checkS2EEmulatorConfiguration(self):

        keys = ["verbose","s2e_binary","gdb_path","gdb_options","klee_options","plugins"]
        s2e_values = self.checkConfiguration(keys, self._analyzer_settings)

        print(s2e_values)

    def checkConfiguration(self, oracles, source):
        out = {}

        for oracle in oracles:
            assert (oracle in self._analyzer_settings["configuration"]), \
                "Bad user settings : Unable to locate analyzer '%s' settings" % oracle
            out[oracle] = self._analyzer_settings["configuration"][oracle]

        return out
