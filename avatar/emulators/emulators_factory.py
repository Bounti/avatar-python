from avatar.emulators.s2e.s2e_emulator import S2EEmulator

import logging

log = logging.getLogger(__name__)

class EmulatorsFactory:

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

            s2e = configuration.checkS2EEmulatorConfiguration()

            qemu = configuration.checkQEmuEmulatorConfiguration()

            return S2EEmulator( a["configuration"],
                            e["configuration"],
                            qemu["base_dir"],
                            qemu["output_dir"])

        elif a['name'] == "klee" :

                log.info("\r\nAttempt to configure Klee analyzer\r\n")

                raise NotImplementedError("Unimplmented Klee analyzer")

        elif a['name'] == "angr" :

                log.info("\r\nAttempt to configure Angr analyzer\r\n")

                raise NotImplementedError("Unimplmented Angr analyzer")
