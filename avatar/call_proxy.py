'''
Created on Jun 24, 2013

@author: Jonas Zaddach <zaddach@eurecom.fr>
'''
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import range
from builtins import int
from builtins import hex
from builtins import str
from future import standard_library
standard_library.install_aliases()
from builtins import object

from collections import defaultdict

class EmulatorTargetCallProxy(object):
    MONITOR_EVENTS = ["emulator_pre_read_request", 
                      "emulator_post_read_request",
                      "emulator_pre_write_request",
                      "emulator_post_write_request"]

    def __init__(self):
        self.__target = None
        self.__monitor_hooks = defaultdict(list)

    def set_target(self, target):
        self.__target = target

    def add_monitor(self, monitor):
        for monitor_event in self.MONITOR_EVENTS:
            if hasattr(monitor, monitor_event):
                self.__monitor_hooks[monitor_event].append(monitor)

    def remove_monitor(self, monitor):
        for (_, monitor_hooks) in self.__monitor_hooks.items():
            try:
                monitor_hooks.remove(monitor)
            except ValueError:
                pass

    def handle_emulator_read_request(self, params):
        assert(self.__target)

        for monitor in self.__monitor_hooks["emulator_pre_read_request"]:
            monitor.emulator_pre_read_request(params)

        params["value"] = self.__target.read_typed_memory(params["address"], params["size"])

        for monitor in self.__monitor_hooks["emulator_post_read_request"]:
            monitor.emulator_post_read_request(params)

        return params["value"]

    def handle_emulator_write_request(self, params):
        assert(self.__target)

        for monitor in self.__monitor_hooks["emulator_pre_write_request"]:
            monitor.emulator_pre_write_request(params)

        self.__target.write_typed_memory(params["address"], params["size"], params["value"])

        for monitor in self.__monitor_hooks["emulator_post_write_request"]:
            monitor.emulator_post_write_request(params)

    def handle_emulator_set_cpu_state_request(self, params):
        # this function sets the CPU state on the target device
        assert(self.__target)

        # TODO: fire events?

        for reg in params["cpu_state"]:
            if reg == "cpsr":
                # skip cpsr register
                continue
            value = int(params["cpu_state"][reg], 16)
            self.__target.set_register(reg, value)

    def handle_emulator_get_cpu_state_request(self, params):
        # this function gets the CPU state on the target device
        assert(self.__target)

        # TODO: fire events?
        ret = {}

        for r in range(13):
            val = self.__target.get_register("r"+str(r))
            ret["cpu_state_"+"r"+str(r)] = hex(val)
        val = self.__target.get_register("sp")
        ret["cpu_state_r13"] = hex(val)
        val = self.__target.get_register("lr")
        ret["cpu_state_r14"] = hex(val)
        val = self.__target.get_register("pc")
        ret["cpu_state_pc"] = hex(val)
        return ret

    def handle_emulator_continue_request(self, params):
        assert(self.__target)

        self.__target.cont()

    def handle_emulator_get_checksum_request(self, params):
        assert(self.__target)

        #cmd = "-gdb-show remote checksum %s %s" % \
        #        (hex(params['address'])[2:], params['size'][2:])
        #return self.__target.execute_gdb_command(cmd)
        return self.__target.get_checksum(\
                params['address'], params['size'])
