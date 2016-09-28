from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import object
import signal
import logging

log = logging.getLogger(__name__)

class AvatarSignal(object):

    @staticmethod
    def handle():
        signal.signal(signal.SIGINT, AvatarSignal.sig_int_handler)

    @staticmethod
    def sig_int_handler(signum, frame):
        log.critical(' --- Ctrl+C Detected --- ')

        from avatar.system import System
        System.getInstance().shutdown()

        log.critical(' --- Waiting for last iteration to complete --- ')
