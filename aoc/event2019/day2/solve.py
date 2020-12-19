########
# PART 1

class Computer(object):
    """
    computer class
    """
    def __init__(self, list):
        self._ip = 0
        self._memory = list

    def update_memory(self, list):
        self._memory = list

    def operation(self, func):
        param1 = self._memory[self._ip + 1]
        param2 = self._memory[self._ip + 2]
        param3 = self._memory[self._ip + 3]
        self._memory[param3] = func(self._memory[param1], self._memory[param2])
        self._ip += 4

    def opcode_1(self):
        self.operation(lambda x, y: x + y)

    def opcode_2(self):
        self.operation(lambda x, y: x * y)

    def opcode_99(self):
        self._ip = -1

    def run_instruction(self):
        #print(self._ip, self._list)
        eval("self.opcode_" + str(self._memory[self._ip]))()

    def run(self):
        self._ip = 0
        while self._ip >= 0:
            self.run_instruction()

    def get_value(self, position):
        return self._memory[position]


with open("event2019/day2/input.txt", "r") as input:
    list = [int(x) for x in input.readline().split(",")]

# replace position 1 with the value 12 
list[1] = 12
# replace position 2 with the value 2
list[2] = 2

computer = Computer(list)

computer.run()
answer = computer.get_value(0)
print("Part 1 =", answer)
assert answer == 3790689 # check with accepted answer

########
# PART 2

with open("event2019/day2/input.txt", "r") as input:
    list = [int(x) for x in input.readline().split(",")]

for noun in range(100):
    for verb in range(100):
        curlist = list[:]

        # replace position 1 with the noun
        curlist[1] = noun
        # replace position 2 with the verb
        curlist[2] = verb

        computer.update_memory(curlist)
        computer.run()

        if (computer.get_value(0) == 19690720):
            answer = 100 * noun + verb
            print("Part 2 =", answer)
            assert answer == 6533 # check with accepted answer
            break
