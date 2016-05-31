class EventWaiter():
    def __init__(self, system):
        self._queue = Queue()

        self._system = system

        self._system.register_event_listener(self._queue_event)

    def _queue_event(self, evt):
        self._queue.put(evt)

    def wait_event(self):
        return self._queue.get()

    def __del__(self):
        self._system.unregister_event_listener(self._queue_event)
