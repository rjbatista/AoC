from event2019.day9.computer_v3 import Computer_v3

########
# PART 1

list = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
assert Computer_v3(list).run([], []) == list
assert len(str(Computer_v3([1102,34915192,34915192,7,4,7,99,0]).run([], [])[0])) == 16
assert Computer_v3([104,1125899906842624,99]).run([], [])[0] == 1125899906842624

with open("event2019/day9/input.txt", "r") as input:
    code = [int(x) for x in input.readline().split(",")]

answer = Computer_v3(code).run([1], [])[0]
print("Part 1 =", answer)
assert answer == 3839402290 # check with accepted answer


########
# PART 2

computer = Computer_v3(code)
computer.set_debug(False)
answer = computer.run([2], [])[0]
print("Part 2 =", answer)
assert answer == 35734 # check with accepted answer
