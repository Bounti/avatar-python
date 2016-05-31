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

        return S2EEmulator( c["s2e"],
                        c["qemu"],
                        c["settings_dir"],
                        c["output_dir"])
