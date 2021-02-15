from event2019.day05.computer import Mode, Colors
from event2019.day07.computer_v2 import Computer_v2

class Computer_v3(Computer_v2):
    def __init__(self, list = []) -> None:
        super().__init__(list)
        self._relative_base = 0
        self._instructions.update({
            '09': { 'name': "set", 'args': 1, 'method': self.opcode_09 },
        })

    def get_debug_param(self, value, mode):
        ret=''
        if (mode != Mode.IMMEDIATE): ret += '['
        if (mode == Mode.RELATIVE): ret += 'base + '
        ret += str(value)
        if (mode != Mode.IMMEDIATE): ret += ']'

        return ret

    def ensure_memory(self, position):
        diff = position - len(self._memory) + 1

        if diff > 0:
            self._memory += [0] * diff

    def microcode_load(self, reg, mode):
        if mode == Mode.POSITION:
            self.ensure_memory(reg)
        elif mode == Mode.RELATIVE:
            self.ensure_memory(self._relative_base + reg)
            return self._memory[self._relative_base + reg]

        return super().microcode_load(reg, mode)

    def microcode_store(self, reg, mode, val):
        if mode == Mode.POSITION:
            self.ensure_memory(reg)
        elif mode == Mode.RELATIVE:
            self.ensure_memory(self._relative_base + reg)
            self._memory[self._relative_base + reg] = val
            return

        super().microcode_store(reg, mode, val)

    def set_memory_value(self, pos, val):
        self.microcode_store(pos, Mode.POSITION, val)

    def opcode_09(self, mode):
        """
        Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter.
        """
        in_arg, _ = self.get_args(1, 0, mode)
        value = in_arg[0]

        self._relative_base += value
        self._ip += 2

        if (self._debug):
            print(Colors.COMMENT, "\t# value =",  value, ", relative_base = ", self._relative_base, end = "")
