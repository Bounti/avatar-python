from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
class Parser(object):

    def checkConfiguration(self, oracles, source):
        out = {}

        for oracle in oracles:
            assert (oracle in self._analyzer_settings["configuration"]), \
                "Bad user settings : Unable to locate analyzer '%s' settings" % oracle
            out[oracle] = self._analyzer_settings["configuration"][oracle]

        return out
