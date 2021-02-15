from queue import Queue
from event2019.day05.computer import Computer, Mode, Colors
from queue import Queue

class Computer_v2(Computer):
    def input(self):
        if isinstance(self._input, Queue):
            return self._input.get()
        else:
            return super().input()

    def output(self, val):
        if isinstance(self._input, Queue):
            self._output.put(val)
        else:
            super().output(val)
