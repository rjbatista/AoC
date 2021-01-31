from enum import Enum

class Colors:
    ADDRESS = '\033[95m'
    MEMORY = '\033[91m'
    OPCODE = '\033[94m'
    COMMENT = '\033[32;1m'
    RESET = '\033[0m'

class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class Computer(object):
    """
    computer class
    """
    def __init__(self, list = []):
        self._orig_code = list
        self._ip = 0
        self._memory = list[:]
        self._input = None
        self._output = None
        self._debug = False
        self._instructions = {
            '01': { 'name': "add", 'args': 3, 'method': self.opcode_01 },
            '02': { 'name': "mul", 'args': 3, 'method': self.opcode_02 },
            '03': { 'name': "in ", 'args': 1, 'method': self.opcode_03 },
            '04': { 'name': "out", 'args': 1, 'method': self.opcode_04 },
            '05': { 'name': "jnz", 'args': 2, 'method': self.opcode_05 },
            '06': { 'name': "jz ", 'args': 2, 'method': self.opcode_06 },
            '07': { 'name': "lt ", 'args': 3, 'method': self.opcode_07 },
            '08': { 'name': "eq ", 'args': 3, 'method': self.opcode_08 },
            '99': { 'name': "halt", 'args': 0, 'method': self.opcode_99 }
        }


    def read_code(fn):
        with open(fn, "r") as file:
            code = [int(x) for x in file.readline().split(",")]

        return code
    

    def load_code(self, fn):
        self._orig_code = Computer.read_code(fn)
        self.reload_code()
    

    def reload_code(self):
        self._memory = self._orig_code[:]


    def set_debug(self, debug):
        self._debug = debug


    def update_memory(self, list):
        self._memory = list[:]


    def get_debug_param(self, value, mode):
        ret=''
        if (mode != Mode.IMMEDIATE): ret += '['
        ret += str(value)
        if (mode != Mode.IMMEDIATE): ret += ']'

        return ret


    def get_args(self, input_argc, output_argc, mode):
        in_args, out_args = [], []
        for i in range(input_argc):
            param = self.microcode_load(self._ip + i + 1, Mode.POSITION)

            in_args.append(self.microcode_load(param, mode[i]))

            if (self._debug):
                if i > 0:
                    print(end = ", ")
                print(self.get_debug_param(param, mode[i]), end = "")

        if (self._debug and output_argc > 0):
            print(end = " => ")

        for i in range(output_argc):
            param = self.microcode_load(self._ip + i + 1 + input_argc, Mode.POSITION)
            param_mode = mode[input_argc + i]

            assert(param_mode != Mode.IMMEDIATE)

            out_args.append((param, param_mode))

            if (self._debug):
                if i > 0:
                    print(end = ", ")
                print(self.get_debug_param(param, param_mode), end = "")

        return in_args, out_args


    def microcode_load(self, reg, mode):
        if mode == Mode.POSITION:
            return self._memory[reg]
        elif mode == Mode.IMMEDIATE:
            return reg
        else:
            raise ValueError("Unknown mode")


    def microcode_store(self, reg, mode, val):
        if mode == Mode.POSITION:
            self._memory[reg] = val
        elif mode == Mode.IMMEDIATE:
            raise ValueError("Illegal mode")
        else:
            raise ValueError("Unknown mode")


    def microcode_3_args(self, func, mode):
        input_args, output_args = self.get_args(2, 1, mode)

        value = func(*input_args)
        out_arg, out_mode = output_args[0]
        self.microcode_store(out_arg, out_mode, value)

        if (self._debug):
            print(Colors.COMMENT, "\t# value =",  value, end = "")

        self._ip += 4


    def microcode_jmp(self, func, mode):
        args, _ = self.get_args(2, 0, mode)

        if func(args[0]): 
            self._ip = args[1]
        else:
            self._ip += 3


    def opcode_01(self, mode):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third position. The three integers immediately after the opcode tell you these three positions - the first two indicate the positions from which you should read the input values, and the third indicates the position at which the output should be stored.
        """
        self.microcode_3_args(lambda x, y: x + y, mode)


    def opcode_02(self, mode):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
        """
        self.microcode_3_args(lambda x, y: x * y, mode)


    def opcode_03(self, mode):
        """
        Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
        """
        _, out_args = self.get_args(0, 1, mode)
        out_arg, out_mode = out_args[0]

        value = self.input()

        self.microcode_store(out_arg, out_mode, value)
        self._ip += 2

        if (self._debug):
            print(Colors.COMMENT, "\t# value =",  value, end = "")


    def opcode_04(self, mode):
        """
        Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
        """
        in_arg, _ = self.get_args(1, 0, mode)
        value = in_arg[0]

        self.output(value)
        self._ip += 2

        if (self._debug):
            print(Colors.COMMENT, "\t# value =",  value, end = "")


    def opcode_05(self, mode):
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        """
        self.microcode_jmp(lambda x : x != 0, mode)


    def opcode_06(self, mode):
        """
        Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        """
        self.microcode_jmp(lambda x : x == 0, mode)


    def opcode_07(self, mode):
        """
        Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        self.microcode_3_args(lambda x, y: 1 if x < y else 0, mode)


    def opcode_08(self, mode):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        self.microcode_3_args(lambda x, y: 1 if x == y else 0, mode)


    def opcode_99(self, _):
        """
        Opcode 99: halt
        """
        self.halt()


    def halt(self):
        """
        Halts
        """
        self._ip = -99


    def run_instruction(self):
        instruction = '%05d' % self._memory[self._ip]
        mode = [Mode(int(x)) for x in instruction[0:3]]
        mode.reverse()
        opcode = instruction[3:]
        instruction_info = self._instructions[opcode]

        if (self._debug):
            print(Colors.ADDRESS, "%4d" % self._ip, ":", end="\t")
            print(Colors.MEMORY, end="")
            print(*self._memory[self._ip:self._ip + instruction_info['args'] + 1], "\t" * (3 - instruction_info['args']), sep="\t", end="")
            print(Colors.OPCODE, end="")
            print(instruction_info['name'], end=" ")

        instruction_info['method'](mode)

        if (self._debug):
            print(Colors.RESET)


    def run(self, input = [], output = []):
        self._ip = 0
        self._input = input
        self._output = output
        while self._ip >= 0:
            self.run_instruction()
        
        return self._output


    def input(self):
        return self._input.pop(0)


    def output(self, val):
        self._output.append(val)


    def get_output(self):
        return self._output
