from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
from avatar.emulators.s2e.s2e_emulator import S2EEmulator
from avatar.emulators.klee.klee_emulator import KleeEmulator

import logging

log = logging.getLogger(__name__)

class EmulatorsFactory(object):

    @staticmethod
    def create(configuration, debug=True):
        """
        Parse the target element from the configuration argument

        :param configuration: dictionary containing all user configuration to correctly setup Avatar modules
        :return:
        """

        a = configuration.checkGlobalAnalyzerConfiguration()

        e = configuration.checkGlobalEmulatorConfiguration()

        if a["name"] == "s2e" :

            log.info("\r\nAttempt to configure S2E analyzer\r\n")

            s2e = configuration.checkS2EEmulatorConfiguration()

            log.info("\r\nAttempt to configure QEmu emulator\r\n")

            qemu = configuration.checkQEmuEmulatorConfiguration()

            return S2EEmulator( a["configuration"],
                            e["configuration"],
                            qemu["base_dir"],
                            qemu["output_dir"])

        elif a['name'] == "klee" :

                log.info("\r\nAttempt to configure Klee analyzer\r\n")

                k = configuration.checkKleeEmulatorConfiguration()

                return KleeEmulator(k["binary"], k["exec_path"], k["base_dir"], k["options"], k["debug"])
                # raise NotImplementedError("Unimplmented Klee analyzer")

        elif a['name'] == "angr" :

                log.info("\r\nAttempt to configure Angr analyzer\r\n")

                raise NotImplementedError("Unimplmented Angr analyzer")
