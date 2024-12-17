""" Advent of code 2024 - day 17 """

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Self

########
# PART 1


class Colors(Enum):
    """ Colors used for dumping the computer state """
    ADDRESS = '\033[95m'
    OPCODE = '\033[94m'
    CODE = '\033[32;1m'
    ERROR = '\033[91m'
    RESET = '\033[0m'


@dataclass
class Computer():
    """ Computer class """

    type Instruction = str

    a: int = 0
    b: int = 0
    c: int = 0
    debug: bool = False
    _ip: int = 0
    _code: list[Instruction] = field(default_factory=list)
    _output: list[int] = field(default_factory=list)

    def load(self: Self, filename: str):
        """ Loads the computer state and code from file """
        self._code = []

        with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
            self.a = int(file.readline().strip().split()[-1])
            self.b = int(file.readline().strip().split()[-1])
            self.c = int(file.readline().strip().split()[-1])
            file.readline()
            self._code = list(map(int, file.readline().strip().split()[-1].split(',')))

            self._ip = 0

    def reset(self):
        """ Reset the computer """
        self.a = 0
        self.b = 0
        self.c = 0
        self._ip = 0
        self._output = []

    def disassembly(self: Self, start: int = 0, length: int = None):
        """ Print the code disassembly """
        def combo_text(operand: int) -> str:
            return ['0', '1', '2', '3', 'A', 'B', 'C'][operand]

        end = (start + length) if length else (len(self._code) - start)

        for ip in range(start, end, 2):
            instr, is_combo = self._decode(ip)
            opcode, operand = self._code[ip:ip + 2]

            if is_combo:
                operand = combo_text(operand)

            print((f"{Colors.ADDRESS.value}{ip:4d}:\t"
                   f"{Colors.OPCODE.value}({opcode}) "
                   f"{Colors.CODE.value}{instr.__name__[8:]} {operand}{Colors.RESET.value}"))

    def run(self: Self):
        """ Run the code """
        self._ip = 0
        while self._ip < len(self._code):
            self._run_instruction()

    def _decode(self: Self, pos: int) -> tuple[Callable[[Self, int], None], bool]:
        opcode = self._code[pos]

        return self._opcode_decoder(opcode), opcode in (0, 2, 5, 6, 7)

    def _run_instruction(self: Self):
        """ run a single instruction """
        if self.debug:
            self.disassembly(self._ip, 1)

        instr, is_combo = self._decode(self._ip)
        operand = self._code[self._ip + 1]

        if is_combo:
            operand = self._combo_decoder(operand)

        instr(operand)

    def _opcode_adv(self: Self, combo: int):
        """
        adv instruction (opcode 0) performs division.
        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer and then
        written to the A register.
        """
        self.a //= (2 ** combo)
        self._ip += 2

    def _opcode_bxl(self: Self, literal: int):
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B
        and the instruction's literal operand, then stores the result in register B.
        """
        self.b ^= literal
        self._ip += 2

    def _opcode_bst(self: Self, combo: int):
        """
        The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        """
        self.b = combo & 0b111
        self._ip += 2

    def _opcode_jnz(self: Self, literal: int):
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0.
        However, if the A register is not zero, it jumps by setting the instruction pointer
        to the value of its literal operand; if this instruction jumps, the instruction pointer
        is not increased by 2 after this instruction.
        """
        if not self.a:
            self._ip += 2
        else:
            self._ip = literal

    def _opcode_bxc(self: Self, _: int):
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        then stores the result in register B.
        (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.b ^= self.c
        self._ip += 2

    def _opcode_out(self: Self, combo: int):
        """
        The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then
        outputs that value. (If a program outputs multiple values, they are separated by commas.)
        """
        self._output.append(combo & 0b111)

        self._ip += 2

    def _opcode_bdv(self: Self, combo: int):
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction except that the result
        is stored in the B register. (The numerator is still read from the A register.)
        """
        self.b = self.a // (2 ** combo)
        self._ip += 2

    def _opcode_cdv(self: Self, combo: int):
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction except that the result
        is stored in the C register. (The numerator is still read from the A register.)
        """
        self.c = self.a // (2 ** combo)
        self._ip += 2

    def _opcode_decoder(self, opcode) -> Callable[[Self, int], None]:
        """ return the code for the specified opcode """
        return [
            self._opcode_adv,
            self._opcode_bxl,
            self._opcode_bst,
            self._opcode_jnz,
            self._opcode_bxc,
            self._opcode_out,
            self._opcode_bdv,
            self._opcode_cdv
        ][opcode]

    def _combo_decoder(self, combo) -> int:
        """ return the value for the specified combo operand """
        # Combo operands 0 through 3 represent literal values 0 through 3.
        if combo <= 3:
            return combo

        # Combo operand 4 represents the value of register A.
        if combo == 4:
            return self.a

        # Combo operand 5 represents the value of register B.
        if combo == 5:
            return self.b

        # Combo operand 6 represents the value of register C.
        if combo == 6:
            return self.c

        # Combo operand 7 is reserved and will not appear in valid programs.
        raise ValueError(combo)

    @property
    def output(self) -> str:
        """ Return the output as a string """

        return ",".join(str(i) for i in self._output)

    @property
    def code_size(self) -> str:
        """ Return the size of the code """

        return len(self._code)

    @property
    def output_size(self) -> str:
        """ Return the size of the code """

        return len(self._output)

    def matches_code(self, pos: int):
        """ Checks if the output matches the code at the specified position """
        return len(self._output) == len(self._code) and self._code[pos] == self._output[pos]


ex1 = Computer()
ex1.load("example1.txt")
ex1.run()
assert ex1.output == "4,6,3,5,6,3,5,2,1,0"

inp = Computer()
inp.load("input.txt")
inp.run()
ANSWER = inp.output
print("Part 1 =", ANSWER)
assert ANSWER == "1,6,3,6,5,6,5,1,7"  # check with accepted answer

########
# PART 2


def find_configuration(computer: Computer):
    """
    Find the configuration that outputs the original code
    Only 3 bits are used for each output -- just find those that match what we want
    """

    def find_configuration_digit(base_number, digit_position):
        for possibility in range(8):
            current_try = base_number + (possibility << 3 * digit_position)

            computer.reset()
            computer.a = current_try
            computer.run()

            if computer.matches_code(digit_position):
                if digit_position == 0:
                    return current_try

                result = find_configuration_digit(current_try, digit_position - 1)
                if not result:
                    # keep trying
                    continue

                return result

        return None

    return find_configuration_digit(0, computer.code_size - 1)


ex2 = Computer()
ex2.load("example2.txt")
# ex2.disassembly()
assert find_configuration(ex2) == 117440

# inp.disassembly()
ANSWER = find_configuration(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 247839653009594  # check with accepted answer
