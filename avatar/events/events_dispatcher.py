from threading import Event, Thread
from queue import Empty, Queue
from avatar.events.event import Event as AvatarEvent
import logging
import sys

log = logging.getLogger(__name__)

class EventsDispatcher(Thread):

    def __init__(self, debug=False):
        super().__init__()
        self._terminating = Event()
        self._debug = debug
        self._events_queue = Queue()
        self._listeners = []

    def start(self):
        super().start()

    def stop(self):
        self._events_queue.put(AvatarEvent.EVENT_SIGABRT)

    def put(self, event):
        if not "properties" in evt:
            evt["properties"] = {}
        self._events_queue.put(event)

    def register_event_listener(self, listener):
        self._listeners.append(listener)

    def unregister_event_listener(self, listener):
        self._listeners.remove(listener)

    def run(self):
        while not self._terminating.is_set():
            try:
                evt = self._events_queue.get(1)

                for listener in self._listeners:
                    try:
                        listener(evt)
                    except Exception:
                        log.exception("Exception while handling event")

                if evt == AvatarEvent.EVENT_SIGABRT:
                    sys.exit(0)
            except Empty:
                pass
            except Exception as ex:
                raise Exception("Some more serious exception handled while processing events. Investigate.")
