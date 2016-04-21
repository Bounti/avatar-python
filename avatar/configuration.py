import os
import logging

log = logging.getLogger(__name__)

class Configuration:

    def getOutputDirectory(self):
        return self.__output_directory

    def __init__(self, user_settings):
        self.__settings = user_settings

        assert (self.__settings["configuration_directory"]), \
            "Bad user settings : Unable to locate 'configuration_directory' settings"
        self.__directory_settings = self.__settings["configuration_directory"]

        assert (self.__settings["symbolic_engine"]), \
        "Bad user settings : Unable to locate 'symbolic_engine' settings"
        self.__symbolic_engine_settings = self.__settings["symbolic_engine"]

        assert (self.__settings["emulator"]), \
            "Bad user settings : Unable to locate 'emulator' settings"
        self.__emulator_settings = self.__settings["emulator"]

        assert (self.__settings["target"]), \
            "Bad user settings : Unable to locate 'target' settings"
        self.__target_settings = self.__settings["target"]

        assert (self.__target_settings["configuration"]), \
            "Bad user settings : Unable to locate openocd target 'configuration' settings"
        self.__target_settings_details = self.__target_settings["configuration"]

        assert (self.__settings["output_directory"]), \
            "Bad user settings : Unable to locate 'output_directory' settings"
        self.__output_directory = self.__settings["output_directory"]

    def checkOpenocdConfiguration(self):

        assert (self.__target_settings_details["config_file"]), \
            "Bad user settings : Unable to locate openocd target 'config_file' settings"
        config_file = self.__target_settings_details["config_file"]

        assert (self.__target_settings_details["host"]), \
            "Bad user settings : Unable to locate openocd target 'host' settings"
        host = self.__target_settings_details["host"]

        assert (self.__target_settings_details["protocol"]), \
            "Bad user settings : Unable to locate openocd target 'protocol' settings"
        protocol = self.__target_settings_details["protocol"]

        assert (self.__target_settings_details["port"]), \
            "Bad user settings : Unable to locate openocd target 'port' settings"
        port = self.__target_settings_details["port"]

        if config_file[0] != '/':
            config_file = self.__directory_settings + '/' + config_file

        return {"config_file": config_file, "host": host, "protocol": protocol, "port": port}

    def checkTargetConfiguration(self):
        assert (self.__target_settings["name"]), \
            "Bad user settings : Unable to locate target 'name' settings"
        name = self.__target_settings["name"]

        assert (self.__target_settings["configuration"]), \
            "Bad user settings : Unable to locate target 'configuration' settings"
        configuration = self.__target_settings["configuration"]

        return {"name":name, "configuration": configuration}
