from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from avatar.configuration.configurationFactory import ConfigurationFactory

from avatar.system import System

import os

#Analyzer Target Emulator tests
ate_tests = {
    "analyzer" :
    {
        "supported" : {"s2e"},
        "unsupported" : {"klee", "angr"},
        "unknown" : {"abc"},
    },
    "target" :
    {
        "supported" : {"openocd", "superspeed-jtag", "gdb"},
        "unsupported" : {},
        "unknown" : {"abc"},
    },
    "emulator" :
    {
        "supported" : {"qemu"},
        "unsupported" : {},
        "unknown" : {"abc"},
    }
}

def generate_conf(analyzer, target, emulator, type):

    analyzer_configuration = {}

    emulator_configuration = {}

    target_configuration = {}

    configuration = {
        "version"                   : 1.0,
        "output_directory"          : "",
        "configuration_directory"   : os.getcwdu(),

        "analyzer"                  : {"name" : analyzer,     "configuration": analyzer_configuration },
        "emulator"                  : {"name" : emulator,    "configuration": emulator_configuration },
        "target"                    : {"name" : target, "configuration": target_configuration },
    }

    return configuration


def test():

    #Test supported, unsupported and unknown configuration
    #Supported should start the element as defined
    #unsupported should raise a NotImplementedError
    #unknown should raise a ValueError

    print("[*] Testing The Configuration module")

    tested_types = {"supported", "unsupported", "unknown"}

    for t in tested_types :

        for analyzer in ate_tests["analyzer"][t] :

            for target in ate_tests["target"][t] :

                for emulator in ate_tests["emulator"][t] :

                    print("    [-] " + analyzer + " " + target  + " " + emulator)

                    try :

                        conf = generate_conf(analyzer, target, emulator, t)

                        configuration = ConfigurationFactory.createParser(conf)

                        # target = TargetsFactory.create(self._configuration)
                        # emulator = EmulatorsFactory.create(self._configuration)

                        # avatar = System(conf, ["--debug", "--trace"])

                        avatar.start()

                        avatar.stop()

                    except (ValueError, NotImplementedError) as e :
                        if type(ex).__name__ == "ValueError" and t == "unknown" :
                            print("        Success")
                        elif type(ex).__name__ == "NotImplementedError" and t == "NotImplementedError" :
                            print("        Success")
                        else :
                            print("Test failed  : "+ type(ex).__name__)
                            print("Test vector : "+ c)
