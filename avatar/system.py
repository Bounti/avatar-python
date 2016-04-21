from threading import Event, Thread
from queue import Empty, Queue

import logging
import sys
import os

from avatar.util.ostools import mkdir_p
from avatar.call_proxy import EmulatorTargetCallProxy
from avatar.configuration import Configuration

#from avatar.emulators.emulator  import Emulator

from avatar.targets.targets_factory import TargetsFactory


CONSOLE_LOG_FORMAT = "%(levelname)s - %(message)s"
FILE_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
#log = logging.getLogger(__module__ + "." + __name__)
log = logging.getLogger(__name__)

class EventWaiter():
    def __init__(self, system):
        self._queue = Queue()
        self._system = system
        system.register_event_listener(self._queue_event)

    def _queue_event(self, evt):
        self._queue.put(evt)

    def wait_event(self):
        return self._queue.get()

    def __del__(self):
        self._system.unregister_event_listener(self._queue_event)

class System():
    """
    Entry point of Avatar Framework
    Setup the entire process according to user configuration

    """

    def __usage(self):
        print("")

    def __parse_options(self, options):
        """
        Parse System contructor options
        :param options: list of options

        :return: none

        """
        for key in options:
            if "--help" in options :
                self.__usage()
            if "--debug" in options :
                self.__debug = True
            if "--trace" in options :
                self.__trace = True

    def __init__(self, user_settings, options=None):
        if options != None :
            if isinstance(options, list) :
                self.__parse_options(options)
            else :
                raise ValueError("Options parameter for System class constructor must be a list")

        self.__configuration = Configuration(user_settings)
        self.__plugins = []
        self.__terminating = Event()
        self.__call_proxy = EmulatorTargetCallProxy()
        self.__listeners = []
        self.__events = Queue()
        self.__event_thread = Thread(target = self.__process_events)
        self.__event_thread.start()
        self.__target = TargetsFactory.create(self.__configuration)
        #self.__emulator = EmulatorsFactory.create(self.__configuration)
        self.is_initialized = False

        output_directory = self.__configuration.getOutputDirectory()

        if os.path.exists(output_directory) and not os.path.isdir(output_directory):
            log.error("Output destination exists, but is not a directory")
            sys.exit(1)

        if not os.path.exists(output_directory):
            log.info("Output directory did not exist, trying to create it")
            mkdir_p(output_directory)

        if os.listdir(output_directory):
            log.warn("Output directory is not empty, will overwrite files")

        file_log_handler = logging.FileHandler(filename = os.path.join(output_directory, "avatar.log"), mode = 'w')
        file_log_handler.setLevel(logging.DEBUG)
        file_log_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))
        logging.getLogger("").addHandler(file_log_handler)

    def __init(self):
        #self.__emulator.init()
        self.__target.init()

        self.is_initialized = True

    def start(self):
        #assert(self.__emulator) #Start emulator hook needs to be set!
        assert(self.__target) #Start target hook needs to be set!

        if self.is_initialized == False :
            self.__init()

        #self.__emulator.set_read_request_handler(self.__call_proxy.handle_emulator_read_request)
        #self.__emulator.set_write_request_handler(self.__call_proxy.handle_emulator_write_request)
        #self.__emulator.set_set_cpu_state_request_handler(self.__call_proxy.handle_emulator_set_cpu_state_request)
        #self.__emulator.set_get_cpu_state_request_handler(self.__call_proxy.handle_emulator_get_cpu_state_request)
        #self.__emulator.set_continue_request_handler(self.__call_proxy.handle_emulator_continue_request)
        #self.__emulator.set_get_checksum_request_handler(self.__call_proxy.handle_emulator_get_checksum_request)
        self.__call_proxy.set_target(self.__target)

        self.__target.start()
        #self.__emulator.start()

    def stop(self):
        if not self.__terminating.is_set():
            self.__terminating.set()
            #self.__emulator.stop()
            self.__target.stop()
            self.__call_proxy.stop_monitors()

    def get_emulator(self):
        return self.__emulator

    def get_target(self):
        return self.__target

    def add_monitor(self, monitor):
        self.__call_proxy.add_monitor(monitor)

    def post_event(self, evt):
        if not "properties" in evt:
            evt["properties"] = {}
        self.__events.put(evt)

    def register_event_listener(self, listener):
        self.__listeners.append(listener)

    def unregister_event_listener(self, listener):
        self.__listeners.remove(listener)

    def __process_events(self):
        while not self.__terminating.is_set():
            try:
                evt = self.__events.get(1)
                log.debug("Processing event: '%s'", str(evt))
                for listener in self.__listeners:
                    try:
                        listener(evt)
                    except Exception:
                        log.exception("Exception while handling event")
            except Empty:
                pass
            except Exception as ex:
                log.exception("Some more serious exception handled while processing events. Investigate.")
                raise ex
