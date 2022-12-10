""" Advent of code 2022 - day XX """
from pathlib import Path
import re

class Computer(object):
    """ computer class """

    def __init__(self):
        self.X = 1
        self.code = []
        self._ip = 0
        self._waiting = 0
        self._current_cycle = 1
        self._microcode = None
        self.trace = False
        self.signal_strengths = []

    def load(self, path):
        """ Load code from path """

        self.code = []
        with path.open("r") as file:
            code_pattern = re.compile(r"^(\w+)(?: (-?\d+))?$")

            for line_number, line in enumerate(file):
                match = code_pattern.match(line)

                if match:
                    func = getattr(self.__class__, "opcode_" + match[1])

                    if match[2] is not None:
                        arg0 = int(match[2])
                    else:
                        arg0 = None

                    # (func, arg0)
                    self.code.append((func, arg0))
                else:
                    raise RuntimeError("invalid input on line %d: %s" % (line_number, line))
        
        return self

    def clock(self):
        """ Run a cycle """

        if self.trace:
            print(f"{self._current_cycle} | X={self.X:5} | {self._waiting} | {self._microcode}")

        if (self._current_cycle + 20) % 40 == 0:
            self.signal_strengths.append(self.signal_strength())

        if self._waiting > 0:
            self._waiting -= 1

        if self._waiting == 0:
            # was running something?
            if self._microcode is not None:
                self._microcode()
                self._microcode = None
            else:
                # get an instruction to run
                func, arg0 = self.code[self._ip]
                self._ip += 1

                if arg0 is not None:
                    func(self, arg0)
                else:
                    func(self)

        self._current_cycle += 1

    def run(self):
        """ Run code """
        while self._ip < len(self.code) or self._microcode is not None:
            self.clock()

    def signal_strength(self):
        return self._current_cycle * self.X

    def opcode_addx(self, arg0):
        """
        addx V takes two cycles to complete.
        After two cycles, the X register is increased by the value V. (V can be negative.)
        """
        def microcode():
            self.X += arg0

        self._waiting = 1
        self._microcode = microcode

    def opcode_noop(self):
        """ noop takes one cycle to complete. It has no other effect. """
        self._waiting = 0


########
# PART 1

ex1 = Computer().load(Path(__file__).parent.joinpath("example1.txt"))
ex1.run()
assert ex1.X == -1

ex2 = Computer().load(Path(__file__).parent.joinpath("example2.txt"))
ex2.run()
assert sum(ex2.signal_strengths) == 13140

inp = Computer().load(Path(__file__).parent.joinpath("input.txt"))
inp.run()
ANSWER = sum(inp.signal_strengths)
print("Part 1 =", ANSWER)
assert ANSWER == 16020 # check with accepted answer

########
# PART 2

class ComputerCrt(Computer):
    def __init__(self):
        super().__init__()
        self._width = 40


    def clock(self):
        beam_x = (self._current_cycle - 1) % self._width
        print("#" if self.X - 1 <= beam_x <= self.X + 1 else ".", end="")

        if beam_x == self._width - 1:
            print()

        return super().clock()

#ex2 = ComputerCrt().load(Path(__file__).parent.joinpath("example2.txt"))
#ex2.run()

inp = ComputerCrt().load(Path(__file__).parent.joinpath("input.txt"))
inp.run()

ANSWER = 'ECZUZALR'
print("Part 2 =", ANSWER)
assert ANSWER == 'ECZUZALR' # check with accepted answer
