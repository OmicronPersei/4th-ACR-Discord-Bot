import threading
import inspect
import asyncio

class ClockSource:
    def __init__(self, update_period):
        self._update_period = int(update_period)
        self.callbacks = []
        self._await_timeout = self._update_period / 2

    def start(self):
        self._set_interval(self._timer_callback, self._update_period)

    def stop(self):
        if self._timer is not None:
            self._timer.cancel()

    def _set_interval(self, func, sec):
        t = threading.Timer(sec, self._timer_callback)
        self._timer = t
        t.start()

    def _timer_callback(self):
        for callback in self.callbacks:
            if inspect.iscoroutinefunction(callback):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(callback())
            else:
                callback()
        self.start()
