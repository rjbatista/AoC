from event2020.day08.computer import Computer, Debugger, ComputerInterruptedError

########
# PART 1
class TraceInstructions(Debugger):
    def __init__(self, computer):
        super().__init__(computer)
        self._trace = set()

    def clear(self):
        self._trace.clear()

    def computer_reset(self):
        self._trace.clear()
        return super().computer_reset()

    def trace(self, instruction, arg):
        if self.computer.ip in self._trace:
            if self.computer._debug:
                print("\033[91mInterrupt at", self.computer.ip, "!\033[0m")
            raise ComputerInterruptedError
        
        self._trace.add(self.computer.ip)

        return super().trace(instruction, arg)

computer = Computer()
debugger = TraceInstructions(computer)
#computer.set_debug(True)
computer.load("event2020/day08/example1.txt")
computer.run()

assert computer.acc == 5

computer.load("event2020/day08/input.txt")
computer.run()

answer = computer.acc
print("Part 1 =", answer)
assert answer == 1654 # check with accepted answer

########
# PART 2

def try_code(possibility):
    instruction, arg = computer.code[possibility]

    if instruction == Computer.opcode_nop:
        computer.code[possibility] = Computer.opcode_jmp, arg
    elif instruction == Computer.opcode_jmp:
        computer.code[possibility] = Computer.opcode_nop, arg

    #computer.disassembly()
    computer.reset()
    computer.run()

    if (not computer.interrupted):
        return computer.acc

    # reset code
    computer.code[possibility] = instruction, arg

    return None

def fix_code():
    for ip, line in enumerate(computer.code):
        if line[0] == Computer.opcode_nop or line[0] == Computer.opcode_jmp:
            ret = try_code(ip)
            if ret is not None:
                return ret

    return None


computer.load("event2020/day08/example1.txt")
assert fix_code() == 8

computer.load("event2020/day08/input.txt")

answer = fix_code()
print("Part 2 =", answer)
assert answer == 833 # check with accepted answer
