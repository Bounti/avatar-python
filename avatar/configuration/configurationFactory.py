from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from future import standard_library
standard_library.install_aliases()
from avatar.configuration.parser.parserV1 import ParserV1
from avatar.configuration.parser.parserV2 import ParserV2

class ConfigurationFactory(object):

    #TODO : use call to create dynamical attribut from fields list
    def getOutputDirectory():
        return self._output_directory

    def __getOutputError(category, field):
        return "Bad user settings : Unable to locate %s '%s' settings" \
            % (category, field)

    @staticmethod
    def createParser(user_settings):
        assert (isinstance(user_settings, dict)), \
            "User settings must be a dictionary"

        if "version" in user_settings :
            version = int(user_settings["version"])
            return ParserV2(user_settings)
        else :
            version = 0.1
            return ParserV1(user_settings)
