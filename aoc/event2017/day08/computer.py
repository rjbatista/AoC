import re

class Computer(object):
    """
    computer class (copied from the one I did on 2020)
    """
    def __init__(self):
        self._code = None
        self._debugger = None
        self.reset()


    def load(self, filename):
        self._code = []
        self.ip = 0
        with open(filename, "r") as file:
            code_pattern = re.compile(r"^(\w+) (inc|dec) (-?\d+) if (\w+) (<=|<|>|>=|!=|==) (-?\d+)$")

            for line_number, line in enumerate(file):
                match = code_pattern.match(line)
                if match:
                    # (func, dest_reg, value, condition_reg, condition, condition_value)
                    self._code.append((getattr(Computer, "opcode_" + match[2]), match[1], int(match[3]), match[4], match[5], match[6]))
                else:
                    raise RuntimeError("invalid input on line %d: %s" % (line_number, line))


    def reset(self):
        self.ip = 0
        self.registers = {}


    def attach(self, debugger):
        self._debugger = debugger


    def opcode_alu(self, operation, dest_reg, value, condition_reg, condition, condition_value):
        result = eval(str(self.registers.get(condition_reg, 0)) + condition + str(condition_value))

        if result:
            self.registers[dest_reg] = operation(self.registers.get(dest_reg, 0), value)

            return self.registers[dest_reg]


    def opcode_inc(self, dest_reg, value, condition_reg, condition, condition_value):
        return self.opcode_alu(lambda r, v: r + v, dest_reg, value, condition_reg, condition, condition_value)


    def opcode_dec(self, dest_reg, value, condition_reg, condition, condition_value):
        return self.opcode_alu(lambda r, v: r - v, dest_reg, value, condition_reg, condition, condition_value)


    def run_instruction(self):
        func, dest_reg, value, condition_reg, condition, condition_value = self._code[self.ip]

        ret = func(self, dest_reg, value, condition_reg, condition, condition_value)

        if (self._debugger):
            self._debugger.trace(func, dest_reg, value, condition_reg, condition, condition_value, ret)


    def run(self):
        self.ip = 0
        self.interrupted = False
        while self.ip < len(self._code):
            self.run_instruction()
            self.ip += 1


class Debugger:
    """
    debugger class - attaches to computer
    """
    def __init__(self, computer):
        self.computer = computer

        computer.attach(self)


    def trace(self, func, dest_reg, value, condition_reg, condition, condition_value, ret):
        pass
