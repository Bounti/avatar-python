from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
from avatar.debuggable import Debuggable

from avatar.events.event import Event

class Emulator(Debuggable):
    def __str__():
        return self.__name

    def __init__(self, name):
        super(Emulator, self).__init__()
        from avatar.system import System

        self.__system = System.getInstance()
        self.__name = name
        self._read_handler = None
        self._write_handler = None
        self._set_cpu_state_handler = None
        self._get_cpu_state_handler = None
        self._continue_handler = None
        self._get_checksum_handler = None

    def set_read_request_handler(self, handler):
        self._read_handler = handler

    def set_write_request_handler(self, handler):
        self._write_handler = handler

    def set_set_cpu_state_request_handler(self, handler):
        self._set_cpu_state_handler = handler

    def set_get_cpu_state_request_handler(self, handler):
        self._get_cpu_state_handler = handler

    def set_continue_request_handler(self, handler):
        self._continue_handler = handler

    def set_get_checksum_request_handler(self, handler):
        self._get_checksum_handler = handler

    def _notify_read_request_handler(self, params):
        self.__system.post_event({"source": "emulator",
                                 "tags": [Event.EVENT_REQUEST_READ_MEMORY_VALUE],
                                 "properties": params})
        assert(self._read_handler) #Read handler must be set at this point

        return self._read_handler(params)

    def _notify_write_request_handler(self, params):
        self.__system.post_event({"source": "emulator",
                                 "tags": [Event.EVENT_REQUEST_WRITE_MEMORY_VALUE],
                                 "properties": params})
        assert(self._write_handler) #Write handler must be set at this point

        return self._write_handler(params)

    def _notify_set_cpu_state_handler(self, params):
        # TODO: we don't have a notify event
        assert(self._set_cpu_state_handler)

        return self._set_cpu_state_handler(params)

    def _notify_get_cpu_state_handler(self, params):
        # TODO: we don't have a notify event
        assert(self._get_cpu_state_handler)

        return self._get_cpu_state_handler(params)

    def _notify_continue_handler(self, params):
        # TODO: we don't have a notify event
        assert(self._continue_handler)

        return self._continue_handler(params)

    def _notify_get_checksum_handler(self, params):
        # TODO: we don't have a notify event
        assert(self._get_checksum_handler)

        return self._get_checksum_handler(params)
