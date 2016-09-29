import logging
import sys
import os
import time
import coloredlogs
import logging
from coloredlogs import NameNormalizer
from humanfriendly import format_table

from avatar.call_proxy import EmulatorTargetCallProxy
from avatar.configuration.configurationFactory import ConfigurationFactory
from avatar.targets.targets_factory import TargetsFactory
from avatar.emulators.emulators_factory import EmulatorsFactory
from avatar.events.event import Event as AvatarEvent
from avatar.events.events_dispatcher import EventsDispatcher
from avatar.events.event_waiter import EventWaiter
from avatar.log import Log
from avatar.signal import AvatarSignal

log = logging.getLogger(__name__)

class System(object):
    """
    Entry point of Avatar Framework
    Setup the entire process according to user configuration

    Singleton Design Pattern to enforce only one instance of System per process
    """

    instance = None

    @staticmethod
    def getInstance():
        if System.instance is None :
            System.instance = System()
        return System.instance

    def is_debug(self):
        return self._debug

    def is_trace(self):
        return self._trace

    def __init__(self, user_settings=None, options=[]):
        assert(System.instance is None), \
            "Only one instance of System is allowed, use getInstance()"
        assert(isinstance(user_settings, dict)), \
            "User_settings parameter for System class constructor must be a dict"
        assert(isinstance(options, list)), \
            "Options parameter for System class constructor must be a list"

        for key in options:
            if "--debug" in options :
                self._debug = True
            if "--trace" in options :
                self._trace = True
        self.is_initialized = False

        System.instance = self

        self._emulator = None
        self._target = None

        try:

            self._configuration = ConfigurationFactory.createParser(user_settings)

            self._target = TargetsFactory.create(self._configuration)
            self._emulator = EmulatorsFactory.create(self._configuration)

            Log.activeLog(self._configuration.getOutputDirectory())

        except (ValueError, AssertionError, OSError, NotImplementedError) as e:
            log.critical("Fail create : %s \r\n" % e)
            sys.exit(0)

        AvatarSignal.handle()

        self._events = EventsDispatcher()
        self._call_proxy = EmulatorTargetCallProxy()
        self._started = True

    def _init(self):

        assert(self._emulator), "The emulator configuration stage may not have been successfully achieved"
        assert(self._target), "The target configuration stage may not have been successfully achieved"

        try :
            self._emulator.init()
            log.info("\r\nAnalyzer initialized : %s\r\n" % str(self._emulator))

            self._target.init()
            log.info("\r\nTarget initialized : %s\r\n" % str(self._target))

            self.is_initialized = True
        except ConnectionRefusedError as e:
            log.critical("Fail to init : \r\n"+str(e)+"\r\n")
            self.stop()

    def start(self):

        assert(self._emulator), "Emulator is not initialized"
        assert(self._target), "Target is not initialized"
        assert(self._events)

        if self.is_initialized == False :
            self._init()

        try:
            self._events.start()
            log.info("Event dispatcher started")

            self._emulator.set_read_request_handler(self._call_proxy.handle_emulator_read_request)
            self._emulator.set_write_request_handler(self._call_proxy.handle_emulator_write_request)
            self._emulator.set_set_cpu_state_request_handler(self._call_proxy.handle_emulator_set_cpu_state_request)
            self._emulator.set_get_cpu_state_request_handler(self._call_proxy.handle_emulator_get_cpu_state_request)
            self._emulator.set_continue_request_handler(self._call_proxy.handle_emulator_continue_request)
            self._emulator.set_get_checksum_request_handler(self._call_proxy.handle_emulator_get_checksum_request)
            self._call_proxy.set_target(self._target)
            log.info("Hook installed")

            self._target.start()
            log.info("Target started")

            self._emulator.start()
            log.info("Emulator started")

            self._started = True
        except (FileNotFoundError, ConnectionRefusedError) as e :
            log.critical("Fail to start : \r\n"+e+"\r\n")
            self.stop()

        nn = NameNormalizer()

        info = {"Version" : "2.0", "compatibility": "1/2", "Testing Support" : "S2E/Klee", "Debugger" : "SuperspeeedJTag/OpenOCD/GDB"}
        log.info("\r\nAvatar : The Dynamic Analysis Framework for Embedded Systems V2.0 : \r\n %s \r\n" % format_table([(nn.normalize_name(n), info[n]) for n in info]))

    def stop(self):
        self._events.stop()
        self._emulator.stop()
        self._target.stop()
        self._started = False
        sys.exit(0)

    """
        Proxy API
    """
    def add_monitor(self, monitor):
        self._call_proxy.add_monitor(monitor)

    """
        EventsDispatcher API
    """
    def register_event_listener(self, listener):
        self._events.append(listener)

    def unregister_event_listener(self, listener):
        self._events.remove(listener)

    def post_event(self, evt):
        self._events.put(evt)

    def get_emulator(self):
        return self._emulator

    def get_target(self):
        return self._target
