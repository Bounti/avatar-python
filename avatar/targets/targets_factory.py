from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from future import standard_library
standard_library.install_aliases()
from avatar.targets.openocd.openocd_target import OpenocdTarget
from avatar.targets.openocd.openocd_jig import OpenocdJig
from avatar.targets.superspeedjtag.superspeed_jtag import SuperspeedJtagTarget
from coloredlogs import NameNormalizer
from humanfriendly import format_table
import logging

log = logging.getLogger(__name__)

class TargetsFactory(object):

    @staticmethod
    def create(configuration, debug=True):
        """
        Parse the target element from the configuration argument

        :param configuration: dictionary containing all user configuration to correctly setup Avatar modules
        :return:
        """
        nn = NameNormalizer()

        c = configuration.checkGlobalTargetConfiguration()

        if c["name"] == "openocd" :

            ini_openocd()

        elif c["name"] == "gdb" :

            raise NotImplementedError("Unimplmented GDB MI target")

            c = configuration.checkGdbConfiguration()

            return GdbserverTarget()

        elif c["name"] == "superspeed-jtag" :

            c = configuration.checkSuperspeedJtagConfiguration()

            return SuperspeedJtagTarget( c['access-port'], c['base_dir'], c['options'], debug=False)

        else :
            raise ValueError("Target configuration wrong : undefined target %s !" % self.name)

    @staticmethod
    def init_openocd():

        c = configuration.checkOpenocdTargetConfiguration()

        if debug:
            log.debug("\r\nTarget configuration : \r\n %s \r\n" % format_table([(nn.normalize_name(n), c[n]) for n in c]))

        if c["protocol"] == "telnet":
            log.info("\r\nAttempt to configure Openocd Telnet target\r\n")

            return OpenocdTarget(c["config_file"], c["host"], int(c["port"]), c["base_dir"], c["exec_path"], c["options"], c["log_stdout"])

        elif  c["protocol"] == "gdb":
            log.info("\r\nAttempt to configure Openocd GDB MI target\r\n")

            return GdbserverTarget(c["config_file"], c["host"], int(c["port"]), c["exec_path"], c["options"], c["log_stdout"])

            raise NotImplementedError("Unimplmented GDB MI connection to Openocd Server")

        elif  c["protocol"] == "gdb_openocd":
            log.info("\r\nAttempt to configure Openocd GDB MI target\r\n")

            openocdjig = OpenocdJig(c["config_file"], c["exec_path"],  c["base_dir"], options=c["options"], debug=debug)

            return GdbserverTarget(c["config_file"], c["host"], int(c["port"]), c["exec_path"], c["options"], c["log_stdout"])

            raise NotImplementedError("Unimplmented GDB MI connection to Openocd Server")

        elif  c["protocol"] == "tcl":

            log.info("\r\nAttempt to configure Openocd TCL target\r\n")

            raise NotImplementedError("Unimplmented TCP TCL connection to Openocd Server")

        else :
            raise ValueError("Target configuration wrong : undefined target protocol %s !" % self.name)

