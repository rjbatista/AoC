from event2019.day9.computer_v3 import Computer_v3

class Computer_v4(Computer_v3):
    def __init__(self, list = []):
        super().__init__(list)
        self._is_waiting_for_input = False
        self._input_processor = None
        self._output_processor = None

    def is_waiting_for_input(self):
        return self._is_waiting_for_input

    def input(self):
        self._is_waiting_for_input = True
        try:
            if self._input_processor:
                return self._input_processor(super().input)
            else:
                return super().input()
        finally:
            self._is_waiting_for_input = False

    def output(self, val):
        if self._output_processor:
            processed = self._output_processor(val)
            if (processed):
                super().output(processed)
        else:
            super().output(val)

    def set_input_processor(self, func):
        self._input_processor = func

    def set_output_processor(self, func):
        self._output_processor = func
