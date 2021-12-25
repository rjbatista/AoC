import re

########
# PART 1

class ALU:
    _registers : list[int]

    def __init__(self) -> None:
        self._input = []
        self._registers = [0] * 4
        self.loaded_code = None
        self._pattern = re.compile(r"^(inp|add|mul|div|mod|eql) ([w-z])(?: (?:(-?\d+)|([w-z])))?$")


    def reset_registers(self):
        self._registers = [0] * 4

        return self


    def __setitem__(self, reg: str, value: int) -> int:
        self._registers[ord(reg) - ord('w')] = value


    def __getitem__(self, reg: str) -> int:
        return self._registers[ord(reg) - ord('w')]


    def load(self, filename):
        with open("event2021/day24/" + filename, "r") as file:
            self.loaded_code = list(line.strip() for line in file.readlines())


    def set_status(self, code, regs):
        self.loaded_code = code[:]
        self._registers = regs[:]


    def load_and_run(self, filename, input = [], reset = True, debug = False):
        self.load(filename)
        self.run_code(input = input, reset = reset, debug = debug)

        return self


    def run_code(self, input = [], reset = True, debug = False):
        if reset:
            self.reset_registers()

        self._input = input
        for ln, instruction in enumerate(self.loaded_code):
            match = self._pattern.match(instruction)

            if match:
                opcode = getattr(ALU, "_opcode_" + match[1])
                arg1 = match[2]
                arg2 = int(match[3]) if match[3] else match[4]

                if arg2 is not None:
                    opcode(self, arg1, arg2)
                else:
                    opcode(self, arg1)

                if debug:
                    print(f"{match[1]}\t{arg1}\t{arg2 if arg2 is not None else ''}\twxyz={self}")
            else:
                raise RuntimeError("Error on line " + str(ln) + ": " + instruction)

        return self


    def __str__(self) -> str:
        return str(self._registers) + str([self._registers[3] // (26*n) for n in range(1, 14)]) + str(self._registers[3] % 26)


    def _opcode_inp(self, a):
        """
        inp a - Read an input value and write it to variable a.
        """
        self[a] = self._input.pop(0)

    
    def _opcode_add(self, a, b):
        """
        add a b - Add the value of a to the value of b, then store the result in variable a.
        """
        self[a] += self[b] if isinstance(b, str) else b


    def _opcode_mul(self, a, b):
        """
        mul a b - Multiply the value of a by the value of b, then store the result in variable a.
        """
        self[a] *= self[b] if isinstance(b, str) else b


    def _opcode_div(self, a, b):
        """
        div a b - Divide the value of a by the value of b, truncate the result to an integer,
        then store the result in variable a.
        (Here, "truncate" means to round the value toward zero.)
        """
        self[a] //= self[b] if isinstance(b, str) else b


    def _opcode_mod(self, a, b):
        """
        mod a b - Divide the value of a by the value of b, then store the remainder in variable a.
        (This is also called the modulo operation.)
        """
        self[a] %= self[b] if isinstance(b, str) else b


    def _opcode_eql(self, a, b):
        """
        eql a b - If the value of a and b are equal, then store the value 1 in variable a.
        Otherwise, store the value 0 in variable a.
        """
        self[a] = 1 if self[a] == (self[b] if isinstance(b, str) else b) else 0


def digits(s):
    return [int(x) for x in s]

#print(digits("99999999999998"))
#print(alu.run_code(input=[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8], debug=True))


def find_pairs():
    alu = ALU()
    alu.load("input.txt")
    total_code = alu.loaded_code[:]

    # break down each digit
    inp_indexes = []
    for i, instruction in enumerate(alu.loaded_code):
        if instruction.startswith('inp'):
            inp_indexes += [i]

    x_value_pattern = re.compile(r"add x (-?\d+)")
    y_value_pattern = re.compile(r"add y (-?\d+)")

    stack = []
    in_push = None
    pairs = []
    for idx, (start, end) in enumerate(zip(inp_indexes, inp_indexes[1:] + [len(alu.loaded_code)])):
        for instr in total_code[start:end]:
            if instr == "div z 1":
                in_push = True
            elif instr == "div z 26":
                in_push = False
            elif instr == "add y 25" or instr == "add y 1":
                continue
            elif in_push and (m := y_value_pattern.match(instr)):
                stack.append((idx, int(m[1])))
            elif not in_push and (m := x_value_pattern.match(instr)):
                pairs.append((stack.pop(), (idx, int(m[1]))))


    return pairs


def maximize(pairs):
    digits = [9] * 14
    for (pa, va), (pb, vb) in pairs:
        while True:
            v = digits[pa] + vb + va
            if 1 <= v <= 9:
                break
            
            digits[pa] -= 1

        digits[pb] = v

    return "".join([str(x) for x in digits])


pairs = find_pairs()
answer = maximize(pairs)
print("Part 1 =", answer)
assert answer == "99298993199873" # check with accepted answer

########
# PART 2

def minimize(pairs):
    digits = [1] * 14
    for (pa, va), (pb, vb) in pairs:
        while True:
            v = digits[pa] + vb + va
            if 1 <= v <= 9:
                break

            digits[pa] += 1

        digits[pb] = v

    return "".join([str(x) for x in digits])

answer = minimize(pairs)
print("Part 2 =", answer)
assert answer == "73181221197111" # check with accepted answer
