from threading import Thread, current_thread
from event2019.day07.computer_v2 import Computer_v2
from itertools import permutations
from queue import Queue

########
# PART 1

def run_setting(show_debug, code, phase_setting):
    computer = Computer_v2()

    computer.set_debug(show_debug)

    input = 0
    for i in range(5):
        computer.update_memory(code)
        input = computer.run([phase_setting[i], input], [])[0]

    return input

# tests
assert run_setting(False, [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0]) == 43210
assert run_setting(False, [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321
assert run_setting(False, [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210

with open("event2019/day07/input.txt", "r") as input:
    code = [int(x) for x in input.readline().split(",")]

answer = max([run_setting(False, code, x) for x in permutations(range(5))])
print("Part 1 =", answer)
assert answer == 77500 # check with accepted answer

########
# PART 2
class ThreadedComputer(Computer_v2):
    def run_instruction(self):
        if (self._debug): print("%9s" % current_thread().name, end="\t")
        super().run_instruction()

    def input(self):
        if (self._debug): print(f"\n\treading from {self._input} with size {self._input.qsize()}")
        return super().input()

    def output(self, val):
        if (self._debug): print(f"\n\twriting to a {self._output} with size {self._output.qsize()}")
        super().output(val)

def run_setting_feedback(show_debug, code, phase_setting):
    threads = []

    computers = []
    for i in range(5):
        computer = ThreadedComputer(code[:])
        computer.set_debug(show_debug)

        computers.append(computer)
        
    first_input = input = Queue()
    output = Queue()
    for i in range(5):
        input.put(phase_setting[i])
        
        # setup first input
        if i == 0: input.put(0)
        
        if (show_debug): print("Creating", i, "with input =", input, "and output =", output)

        t = Thread(target=computers[i].run, daemon=True, args=(input, output))
        threads.append(t)

        input = output
        if (i < 3):
            output = Queue()
        elif (i == 3):
            output = first_input

    for i in range(5):
        threads[i].start()

    for i in range(5):
        while (threads[i].is_alive()):
            threads[i].join(1)

    last = None
    #output = computers[4].get_output()
    while not first_input.empty():
        last = first_input.get()

    return last


assert run_setting_feedback(False, [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729

assert run_setting_feedback(False, [
    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216

answer = max([run_setting_feedback(False, code, x) for x in permutations(range(5, 10))])
print("Part 2 =", answer)
assert answer == 22476942 # check with accepted answer
