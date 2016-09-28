from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import int
from future import standard_library
standard_library.install_aliases()
from avatar.targets.target import Target
from avatar.targets.openocd.openocd_jig import OpenocdJig

import socket
import logging
import telnetlib
import time

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

class OpenocdTarget(Target):
    """
    This module includes the logic to talk with OpenOCD in order to
    perform low-level actions on the target.
    Methods are split in three classes, according to their decorator:
        * paused: stop the target before performing actions, then resume it
        * halted: stop the target to perform actions
        * raw: plain naked actions
    """

    def __init__(self, fname, host, port, base_dir, exec_path="openocd", options="", debug=False):
        self._name = "Openocd [%s:%d]" % (host,port)
        self._host = host
        self._port = port
        self._base_dir = base_dir
        self._exec_path = exec_path
        self._debug = debug
        self._prompt = None
        self._base_dir = base_dir
        self._openocdjig = OpenocdJig(fname, exec_path, base_dir, options=options, debug=self._debug)
        self._connected = False

    def __str__(self):
        return self._name

    def init(self):
        pass

    def start(self):
        if self._connected is not True:
            self._openocdjig.attach()

            if self._prompt == None :

                timeout = 0
                while not self._connected :
                    try :
                        log.info("Trying to connect to target openocd server at %s:%d", self._host, self._port)
                        self._prompt = telnetlib.Telnet(self._host,self._port)
                        self._connected = True
                    except ConnectionRefusedError as e:
                        log.warning("Unable to connect to target openocd server at %s:%d (%d)", self._host, self._port, timeout)
                        timeout = timeout + 1
                        time.sleep(2)
                        if timeout > 5 :
                            log.error("Please check Openocd log for more details.")
                            raise ConnectionRefusedError("Unable to connect to openocd, please check openocd logs : %s " % self._base_dir+"/openocd_std.log")

            self.get_output()


    def stop(self):
        """ Stop the telnet session to OpenOCD """
        if self._connected is True :

            self._prompt.write(str("exit"+'\n').encode("ascii"))

            self._prompt.close()

            del self._prompt

            self._openocdjig.detach()

            self._connected = False

    def wait(self):
        self.get_output()

    def get_output(self, timeout=0):
        """
        Get the output of last command
        :param to: timeout in seconds (optional)
        :type to: int
        """
        if timeout == 0:
            out = str(self._prompt.read_until(b"> "))
        else:
            out = str(self._prompt.read_until(b"> ", timeout))
        out = out.split("> ")[0]
        return out

###################################################################
## Raw naked methods
###################################################################

    def halt(self):
        """ Stop the target """
        self.raw_cmd("halt", False)

    def cont(self):
        """ Resume the target """
        self.raw_cmd("resume", False)

    def get_checksum(self, addr, size):
        return raw_cmd("checksum %s %d" % (addr, size))

    def raw_cmd(self, cmd, is_log=True):
        """
        Send a raw command to OpenOCD
        :param cmd: an OpenOCD command
        :type cmd: str
        :param is_log: whether to log command output (optional, default True)
        :type is_log: bool
        """
        self._prompt.write(str(cmd+'\n').encode("ascii"))
        out = self.get_output()
        #if is_log:
        #    log.info(out)
        return out

    def write_typed_memory(self, address, size, data):
        cmd = ""
        if size == 8 :
            cmd = "mwb"
        if size == 16 :
            cmd = "mwh"
        if size == 32 :
            cmd = "mww"

        assert( cmd != "" ), \
            "invalid argument '%d' for size in write_typed_memory, accepted 8, 16, 32" % size
        self.raw_cmd(cmd+" %s %s" % (address, data))

    def read_typed_memory(self, address, size):

        cmd = ""
        if size == 8 :
            cmd = "mdb"
        if size == 16 :
            cmd = "mdh"
        if size == 32 :
            cmd = "mdw"

        assert( cmd != "" ), \
            "invalid argument '%d' for size in write_typed_memory, accepted 8, 16, 32" % size
        self.raw_cmd(cmd+" %s" % address)

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
		# FIXME: hardcoded hw breakpoint
        self.raw_cmd("bp %s %d hw" % (addr, size))

    def remove_raw_bp(self, addr):
        """
        Remove a breakpoint
        :param addr: address literal in hexadecimal
        :type addr: str
        """
        self.raw_cmd("rbp %s" % addr)

    def get_raw_register(self, regname):
        """
        Read a single register, allowed values within ARM_REGISTERS
        :param regname: register name (see ARM_REGISTERS)
        :type regname: str
        :return: value register in hexadecimal
        :rtype: str
        """
        value = self.raw_cmd("reg " + regname, False)

        assert("not found" not in value), "Register '%s' not found in current target " % regname

        value = value.split(": ")[1][:10]

        return int(value, 0)

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
