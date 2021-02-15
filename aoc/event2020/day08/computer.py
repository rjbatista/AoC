import re

class Colors:
    ADDRESS = '\033[95m'
    OPCODE = '\033[94m'
    COMMENT = '\033[32;1m'
    ERROR = '\033[91m'
    RESET = '\033[0m'

class Computer(object):
    """
    computer class
    """
    def __init__(self):
        self.ip = 0
        self.acc = 0
        self.interrupted = False
        self.code = None
        self._debug = False
        self._debugger = None

    def reset(self):
        self.ip = 0
        self.acc = 0
        self.interrupted = False
        if self._debugger:
            self._debugger.computer_reset()

    def load(self, file):
        self.code = []
        self.reset()
        with open(file, "r") as file:
            code_pattern = re.compile(r"^(\w+)\s+([+-]\d+)$")
            for line in file:
                m = code_pattern.match(line)
                if m:
                    self.code.append((getattr(Computer, "opcode_" + m.group(1)), int(m.group(2))))
                else:
                    raise RuntimeError("invalid input " + line)

    def disassembly(self):
        for ip, (instruction, arg) in enumerate(self.code):
            print(Colors.ADDRESS, "%4d" % ip, ":", end="\t")
            print(Colors.OPCODE, instruction.__name__[7:], arg, end="")
            print(Colors.RESET)

    def set_debug(self, debug):
        self._debug = debug

    def opcode_nop(self, arg):
        """
        stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
        """
        self.ip += 1

    def opcode_acc(self, arg):
        """
        increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
        """
        self.acc += arg
        self.ip += 1

    def opcode_jmp(self, arg):
        """
        jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
        """
        self.ip += arg

    def run_instruction(self):
        if self._debug:
            print(Colors.ADDRESS, "%4d" % self.ip, ":", end="\t")

        instruction, arg = self.code[self.ip]

        if self._debug:
            print(Colors.OPCODE, instruction.__name__[7:], arg, end="")
            print(Colors.RESET)

        if self._debugger:
            self._debugger.trace(instruction, arg)

        instruction(self, arg)

    def run(self):
        self.ip = 0
        self.interrupted = False
        while self.ip < len(self.code):
            try:
                self.run_instruction()
            except ComputerInterruptedError:
                self.interrupted = True
                break

    def attach(self, debugger):
        self._debugger = debugger

class Debugger:
    """
    debbuger class - attaches to computer
    """
    def __init__(self, computer):
        self.computer = computer
        computer.attach(self)

    def computer_reset(self):
        pass

    def trace(self, instruction, arg):
        pass

class ComputerInterruptedError(Exception):
    pass
