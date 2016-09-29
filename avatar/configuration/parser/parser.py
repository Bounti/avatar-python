class Parser(object):

    def checkConfiguration(self, oracles, source):
        out = {}

        for oracle in oracles:
            assert (oracle in self._analyzer_settings["configuration"]), \
                "Bad user settings : Unable to locate analyzer '%s' settings" % oracle
            out[oracle] = self._analyzer_settings["configuration"][oracle]

        return out
