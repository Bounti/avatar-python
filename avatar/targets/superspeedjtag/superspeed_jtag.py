from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from future import standard_library
standard_library.install_aliases()
from avatar.targets.target import Target

import socket
import logging
import telnetlib
import time
from ctypes import cdll

log = logging.getLogger(__name__)

# Decorator for methods requiring target Stop&Start
def paused(fn):
    # TODO: variadic decorator
    def wrapped(self, opt=None):
        self.halt()
        if opt:
          fn(self, opt)
        else:
          fn(self)
        self.cont()
    return wrapped

# Decorator for methods requiring target Hard Stop
def halted(fn):
    # TODO: variadic decorator
    def wrapped(self, opt=None):
        self.halt()
        if opt:
          return fn(self, opt)
        else:
          return fn(self)
    return wrapped

class SuperspeedJtagTarget(Target):
    """
    This module includes the logic to talk with SuperspeedJtag in order to
    perform low-level actions on the target.
    Methods are split in three classes, according to their decorator:
        * paused: stop the target before performing actions, then resume it
        * halted: stop the target to perform actions
        * raw: plain naked actions
    """

    def __init__(self, ap, base_dir, options="", debug=False):
        self._name = "SuperspeedJtag (%s)" % (ap)
        self._ap = ap
        self._base_dir = base_dir
        self._debug = debug
        self._prompt = None
        self._base_dir = base_dir
        self._connected = False
        self.lib = cdll.LoadLibrary('lib/libsuperspeed-jtag.so')
        self.obj = None

        if self.lib == None :
            raise Exception("Unable to load dynamic library : libsuperspeed-jtag.so")

    def __str__(self):
        return self._name

    def init(self):
        pass

    def start(self):
        if self._connected is not True:
            self.obj = self.lib.jtag_init()

    def stop(self):
        """ Stop the Jtag device """
        if self._connected is True :

            self.lib.jtag_close(self.obj)

            self._connected = False

###################################################################
## Raw naked methods
###################################################################

    def halt(self):
        """ Stop the target """
        self.lib.jtag_halt(self.obj)

    def cont(self):
        """ Resume the target """
        self.lib.jtag_resume(self.obj)

    def get_checksum(self, addr, size):
        return self.lib.jtag_checksum(self.obj, addr, size)

    def write_typed_memory(self, address, size, data):

        self.lib.jtag_write(self.obj, address, data)

    def read_typed_memory(self, address, size):

        self.lib.jtag_read(self.obj, address)

    def set_breakpoint(self, address, **properties):
        self.put_raw_bp(address, 2)

    def remove_breakpoint(self, address):
        self.remove_raw_bp(address)

    def put_raw_bp(self, addr, size):
        """
        Put a breakpoint
        :param addr: address literal in hexadecimal
        :type addr: str
        :param size: brakpoint size
        :type size: integer
        """
        self.lib.bp(self.obj, addr, size)

    def remove_raw_bp(self, addr):
        """
        Remove a breakpoint
        :param addr: address literal in hexadecimal
        :type addr: str
        """
        self.lib.remove_bp(self.obj, addr, size)

    def get_raw_register(self, regname):
        """
        Read a single register, allowed values within ARM_REGISTERS
        :param regname: register name (see ARM_REGISTERS)
        :type regname: str
        :return: value register in hexadecimal
        :rtype: str
        """
        return self.lib.raw_register(self.obj, regname)

    def initstate(self, cfg):
        """ Change S2E configurable machine initial setup"""
        assert("machine_configuration" in cfg)
        self.get_output(2)
        st = self.dump_all_registers()
        cfg["machine_configuration"]["init_state"] = [st]
        # Override entry address
        if "pc" in st:
            cfg["machine_configuration"]["entry_address"] = st["pc"]
        return cfg

###################################################################
## Paused methods
###################################################################

    @paused
    def put_bp(self, addr):
        """
        Pause the target, put a breakpoint, then resume it
        :param addr: address literal in hexadecimal
        :type addr: str
        """
		# XXX: hardcoded: thumb, hw breakpoint
        self.raw_cmd("bp %s 2 hw" % addr)

    @paused
    def remove_bp(self, addr):
        """
        Pause the target, remove a breakpoint, the resume it
        :param addr: address literal in hexadecimal
        :type addr: str
        """
        self.remove_raw_bp(addr)

    @paused
    def get_register(self, regname):
        """
        Pause the target, read a single register, then resume it
        :param regname: register name (allowed values within ARM_REGISTERS)
        :type regname: str
        :return: value register in hexadecimal
        :rtype: str
        """
        return self.get_raw_register(regname)

###################################################################
## Halted methods
###################################################################

    @halted
    def dump_all_registers(self):
        """
        Halt the target, loop over all available registers
        and dump their content
        :return: dict of regname->value
        :rtype: dict of str->str
        """
        out = {}
        # Flush session input
        self.get_output(2)

        try:
            for i in ARM_REGISTERS:
                val = self.get_raw_register(i)
                try:
                    out[i] = int(val, 0)
                except Exception as ex:
                    log.exception("%s ignored, read value was «%s»" % (i, val))
                    continue
        except Exception as e:
            log.critical(e)
            return {}
        return out

###################################################################
## Class methods
###################################################################

    @classmethod
    def from_str(cls, sockaddr_str):
        """ Static factory """
        assert(sockaddr_str.startswith("tcp:"))
        sockaddr = (sockaddr_str[:sockaddr_str.rfind(":")],
                    int(sockaddr_str[sockaddr_str.rfind(":") + 1:]))
        return cls(sockaddr)
