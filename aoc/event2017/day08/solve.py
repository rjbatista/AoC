from types import TracebackType
from event2017.day08.computer import Computer, Debugger

########
# PART 1

ex_computer = Computer()
ex_computer.load("event2017/day08/example1.txt")
ex_computer.run()

assert max(ex_computer.registers.values()) == 1

computer = Computer()
computer.load("event2017/day08/input.txt")
computer.run()
answer = max(computer.registers.values())
print("Part 1 =", answer)
assert answer == 5966 # check with accepted answer


########
# PART 2

class CheckMaxRegDebugger(Debugger):
    def __init__(self, computer):
        super().__init__(computer)
        self.max_reg_value = 0


    def trace(self, func, dest_reg, value, condition_reg, condition, condition_value, ret):
        if ret:
            self.max_reg_value = max(self.max_reg_value, ret)

        return super().trace(func, dest_reg, value, condition_reg, condition, condition_value, ret)



ex_debugger = CheckMaxRegDebugger(ex_computer)
ex_computer.reset()
ex_computer.run()

assert ex_debugger.max_reg_value == 10


debugger = CheckMaxRegDebugger(computer)
computer.reset()
computer.run()


answer = debugger.max_reg_value
print("Part 2 =", answer)
assert answer == 6347 # check with accepted answer
