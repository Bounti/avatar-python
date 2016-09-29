'''
Created on Jun 24, 2013

@author: Jonas Zaddach <zaddach@eurecom.fr>
'''
from avatar.targets.target import Target
import logging
from avatar.bintools.gdb.gdb_debugger import GdbDebugger
from avatar.event import Event
from avatar.bintools.gdb.mi_parser import Async
from avatar.debuggable import Breakpoint
from queue import Queue

log = logging.getLogger(__name__)

class GdbBreakpoint(Breakpoint):
    def __init__(self, system, bkpt_num):
        super().__init__()
        self._system = system
        self._bkpt_num = bkpt_num
        self._queue = Queue()
        system.register_event_listener(self._event_receiver)

    def wait(self, timeout = None):
        if self._handler:
            raise Exception("Breakpoint cannot have a handler and be waited on")

        if timeout == 0:
            return self._queue.get(False)
        else:
            return self._queue.get(True, timeout)

    def delete(self):
        self._system.unregister_event_listener(self._event_receiver)
        self._system.get_target()._gdb_interface.delete_breakpoint(self._bkpt_num)

    def _event_receiver(self, evt):
        if Event.EVENT_BREAKPOINT in evt["tags"] and \
                evt["source"] == "target" and \
                evt["properties"]["bkpt_number"] == self._bkpt_num:
            if self._handler:
                self._handler(self._system, self)
            else:
                self._queue.put(evt)
        elif Event.EVENT_SIGABRT in evt["tags"]:
                self._queue.put(evt)

class GdbserverTarget(Target):
    def __init__(self, host, port, exec_path="gdb", options=[], log_stdout=False, fname=None):
        self._port = port
        self._host = host
        self._config_file = config_file
        self._exec_path = exec_path
        self._options = options
        self._log_stdout = log_stdout
        self._fname = fname

    def start(self):
        #TODO: Handle timeout

        if self._exec_path != "gdb" :
            log.warn("target_gdb_path not defined in avatar configuration, using hardcoded GDB path: %s", self._exec_path)

        if  System(None).is_debug :
            log.info("Trying to connect to target gdb server at %s:%d", self._host, self._port)

        self._gdb_interface = GdbDebugger(gdb_executable = self._exec_path, cwd = ".", additional_args = self._options )
        self._gdb_interface.set_async_message_handler(self.handle_gdb_async_message)

        not_started = False

        while not_started :
            try:
                self._gdb_interface.connect(("tcp", self._host, "%d" % self._port))
                not_started = True
            except TimeoutError :
                if  System(None).is_debug :
                    log.info("Timeout... Connecting to %s:%d again ", self._host, self._port)
                continue

    def write_typed_memory(self, address, size, data):
        self._gdb_interface.write_memory(address, size, data)

    def read_typed_memory(self, address, size):
        return self._gdb_interface.read_memory(address, size)

    def set_register(self, reg, val):
        self._gdb_interface.set_register(reg, val)

    def get_register(self, reg):
        return self._gdb_interface.get_register(reg)

    def get_register_from_nr(self, num):
        try:
            return self.get_register(["r0", "r1", "r2", "r3", "r4", "r5",
                "r6", "r7", "r8", "r9", "r10",
                "r11", "r12", "sp", "lr", "pc", "cpsr"][num])
        except IndexError:
            log.warn("get_register_from_nr called with unexpected register index %d", num)
            return 0

    def execute_gdb_command(self, cmd):
        return self._gdb_interface.execute_gdb_command(cmd)

    def get_checksum(self, addr, size):
        return self._gdb_interface.get_checksum(addr, size)

    def stop(self):
        pass

    def set_breakpoint(self, address, **properties):
        if "thumb" in properties:
            del properties["thumb"]
        bkpt = self._gdb_interface.insert_breakpoint(address, *properties)
        return GdbBreakpoint(self._system, int(bkpt["bkpt"]["number"]))

    def cont(self):
        self._gdb_interface.cont()

    def handle_gdb_async_message(self, msg):
        print("Received async message: '%s'" % str(msg))
        if msg.type == Async.EXEC:
            if msg.klass == "running":
                self._post_event({"tags": [Event.EVENT_RUNNING], "channel": "gdb"})
            elif msg.klass == "stopped":
                if "reason" in msg.results and msg.results["reason"] == "breakpoint-hit":
                    self._post_event({"tags": [Event.EVENT_STOPPED, Event.EVENT_BREAKPOINT],
                                     "properties": {
                                        "address": int(msg.results["frame"]["addr"], 16),
                                        "bkpt_number": int(msg.results["bkptno"])},
                                     "channel": "gdb"})
                elif "reason" in msg.results and msg.results["reason"] == "signal-received":
                    # this is data abort
                    try:
                        addr = int(msg.results["frame"]["addr"], 16)
                    except:
                        addr = 0xDEADDEAD
                    self._post_event({"tags": [Event.EVENT_STOPPED, Event.EVENT_SIGABRT],
                        "properties": {
                            "address": addr,
                            },
                        "channel": "gdb"})

    def _post_event(self, evt):
        evt["source"] = "target"
        self._system.post_event(evt)

    @classmethod
    def from_str(cls, sockaddr_str):
        assert(sockaddr_str.startswith("tcp:"))
        sockaddr = (sockaddr_str[:sockaddr_str.rfind(":")],
                    int(sockaddr_str[sockaddr_str.rfind(":") + 1:]))
        return cls(sockaddr)
