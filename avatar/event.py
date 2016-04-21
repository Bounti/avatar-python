from enum import Enum


class Event(Enum):

    """
        Defines Avatar events
    """
    EVENT_STOPPED = "EVENT_STOPPED"

    EVENT_BREAKPOINT = "EVENT_BREAKPOINT"

    EVENT_END_STEPPING = "EVENT_END_STEPPING"

    EVENT_RUNNING = "EVENT_RUNNING"

    EVENT_REQUEST_READ_MEMORY_VALUE = "EVENT_REQUEST_READ_MEMORY_VALUE"

    EVENT_REQUEST_WRITE_MEMORY_VALUE = "EVENT_REQUEST_WRITE_MEMORY_VALUE"

    EVENT_RESPONSE_READ_MEMORY_VALUE = "EVENT_RESPONSE_READ_MEMORY_VALUE"

    EVENT_RESPONSE_WRITE_MEMORY_VALUE = "EVENT_RESPONSE_WRITE_MEMORY_VALUE"

    EVENT_SIGABRT = "EVENT_SIGABRT"
