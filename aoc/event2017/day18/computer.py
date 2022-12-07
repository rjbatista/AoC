""" Advent of code 2017 - day 18 - Computer class """
import re
from collections import defaultdict

class Computer(object):
    """ computer class (copied from the one I did on 2020) """
    def __init__(self):
        self._registers = defaultdict(lambda : 0)
        self._sound = None
        self.code = []
        self._ip = 0

    def load(self, path):
        """ Load code from path """

        self.code = []
        with path.open("r") as file:
            code_pattern = re.compile(r"^(\w{3}) (?:([a-z])|(-?\d+))(?: ([a-z])| (-?\d+))?$")

            for line_number, line in enumerate(file):
                match = code_pattern.match(line)

                if match:
                    # (func, arg0, arg1)

                    func = getattr(self.__class__, "opcode_" + match[1])

                    if match[3] is not None:
                        arg0 = int(match[3])
                    else:
                        arg0 = match[2]

                    if match[5] is not None:
                        arg1 = int(match[5])
                    else:
                        arg1 = match[4]

                    self.code.append((func, arg0, arg1))
                else:
                    raise RuntimeError("invalid input on line %d: %s" % (line_number, line))

    def run(self):
        """ Code until recover is triggered """
        self._ip = 0

        return self._resume()

    def _resume(self):
        """ resume computation """

        while self._ip < len(self.code):
            func, arg0, arg1 = self.code[self._ip]
            self._ip += 1

            if arg1 is not None:
                func(self, arg0, arg1)
            else:
                recover = func(self, arg0)

                if recover:
                    return recover

    def opcode_snd(self, arg0):
        """ snd X plays a sound with a frequency equal to the value of X. """

        if not isinstance(arg0, int):
            arg0 = self._registers[arg0]

        self._sound = arg0

    def opcode_set(self, reg, val):
        """ set X Y sets register X to the value of Y. """

        if not isinstance(val, int):
            val = self._registers[val]

        self._registers[reg] = val

    def opcode_add(self, reg, val):
        """ add X Y increases register X by the value of Y. """

        if not isinstance(val, int):
            val = self._registers[val]

        self._registers[reg] += val

    def opcode_mul(self, reg, val):
        """
        mul X Y sets register X to the result of multiplying
        the value contained in register X by the value of Y.
        """

        if not isinstance(val, int):
            val = self._registers[val]

        self._registers[reg] *= val

    def opcode_mod(self, reg, val):
        """
        mod X Y sets register X to the remainder of dividing
        the value contained in register X by the value of Y
        (that is, it sets X to the result of X modulo Y).
        """

        if not isinstance(val, int):
            val = self._registers[val]

        self._registers[reg] %= val

    def opcode_rcv(self, arg0):
        """
        rcv X recovers the frequency of the last sound played,
        but only when the value of X is not zero.
        (If it is zero, the command does nothing.)
        """
        if not isinstance(arg0, int):
            arg0 = self._registers[arg0]

        if arg0 != 0:
            return self._sound

        return None

    def opcode_jgz(self, arg0, arg1):
        """
        jgz X Y jumps with an offset of the value of Y,
        but only if the value of X is greater than zero.
        (An offset of 2 skips the next instruction,
        an offset of -1 jumps to the previous instruction,
        and so on.)
        """
        if not isinstance(arg0, int):
            arg0 = self._registers[arg0]

        if arg0 > 0:
            if not isinstance(arg1, int):
                arg1 = self._registers[arg1]

            self._ip += arg1 - 1
