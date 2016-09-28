from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
import sys
import os
import logging
import coloredlogs
from avatar.util.ostools import mkdir_p

CONSOLE_LOG_FORMAT = "%(levelname)s - %(message)s"
FILE_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

coloredlogs.DEFAULT_LOG_FORMAT = "[%(levelname)s]%(message)s"

coloredlogs.DEFAULT_LEVEL_STYLES = {
    'info': {'color': 'blue'},
    'critical': {'color': 'red', 'bold': True},
    'verbose': {'color': 'blue'},
    'error': {'color': 'red'},
    'debug': {'color': 'green'},
    'warning': {'color': 'yellow'}}

coloredlogs.DEFAULT_FIELD_STYLES = {
    'hostname': {'color': 'magenta'},
    'programname': {'color': 'cyan'},
    'name': {'color': 'blue'},
    'levelname': {'color': 'cyan', 'bold': True},
    'asctime': {'color': 'green'}}

coloredlogs.install(level='DEBUG')

log = logging.getLogger(__name__)

class Log(object):

    def activeLog(output_directory):
        if os.path.exists(output_directory) and not os.path.isdir(output_directory):
            raise Exception("\r\nOutput destination exists, but is not a directory\r\n")

        if not os.path.exists(output_directory):
            log.info("\r\nOutput directory did not exist, trying to create it\r\n")
            mkdir_p(output_directory)

        if os.listdir(output_directory):
            log.warn("\r\nOutput directory is not empty, will overwrite files\r\n")

        file_log_handler = logging.FileHandler(filename = os.path.join(output_directory, "avatar.log"), mode = 'w')
        file_log_handler.setLevel(logging.DEBUG)
        file_log_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))
        logging.getLogger("").addHandler(file_log_handler)
