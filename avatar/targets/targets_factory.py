from avatar.targets.openocd.openocd_target import OpenocdTarget
from avatar.targets.openocd.openocd_jig import OpenocdJig

class TargetsFactory:

    def __init__(self):
        pass

    @staticmethod
    def create(configuration):
        """
        Parse the target element from the configuration argument

        :param configuration: dictionary containing all user configuration to correctly setup Avatar modules
        :return:
        """

        conf = configuration.checkTargetConfiguration()

        if conf["name"] == "openocd" :
            conf = configuration.checkOpenocdConfiguration()

            if conf["protocol"] == "telnet" :
                return OpenocdTarget(conf["config_file"], conf["host"], int(conf["port"]))
            elif  conf["protocol"] == "gdb":
                NotImplementedError("Unimplmented GDB MI connection to Openocd Server")
            elif  conf["protocol"] == "tcl":
                NotImplementedError("Unimplmented TCP TCL connection to Openocd Server")
            else :
                raise ValueError("Target configuration wrong : undefined target protocol %s !" % self.name)

        elif conf["name"] == "gdb" :
            raise NotImplementedError("Unimplmented GDB MI target")
        else :
            raise ValueError("Target configuration wrong : undefined target %s !" % self.name)
