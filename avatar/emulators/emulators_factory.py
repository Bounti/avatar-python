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

        c = configuration.checkEmulatorConfiguration()

        if c["analyzer"]["name"] == "s2e" :

            return S2EEmulator( c["analyzer"]["configuration"],
                            c["emulator"]["configuration"],
                            c["settings_dir"],
                            c["output_dir"])

        elif c["analyzer"]['name'] == "klee" :

                log.info("\r\nAttempt to configure Klee analyzer\r\n")

                raise NotImplementedError("Unimplmented Klee analyzer")

        elif c["analyzer"]['name'] == "angr" :

                log.info("\r\nAttempt to configure Angr analyzer\r\n")

                raise NotImplementedError("Unimplmented Angr analyzer")
