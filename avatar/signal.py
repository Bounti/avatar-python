import signal
import logging

log = logging.getLogger(__name__)

class AvatarSignal:

    @staticmethod
    def handle():
        signal.signal(signal.SIGINT, AvatarSignal.sig_int_handler)

    @staticmethod
    def sig_int_handler(signum, frame):
        log.critical(' --- Ctrl+C Detected --- ')

        from avatar.system import System
        System.getInstance().shutdown()

        log.critical(' --- Waiting for last iteration to complete --- ')
