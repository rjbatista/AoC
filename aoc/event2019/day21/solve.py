from event2019.day13.computer_v4 import Computer_v4

########
# PART 1

def console_write(val):
    try:
        print(chr(val), end="")
        return None
    except ValueError:
        # must be the result!
        return val


def ascii_input(func):
    return ord(func())


# Two registers are available: T, the temporary value register, and J, the jump register.
#
# Your springdroid can detect ground at four distances: one tile away (A), two tiles away (B), three tiles away (C), and four tiles away (D).
#
# AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
# OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
# NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.


# J = (!C & D) | !A
springscript = """NOT C J
AND D J
NOT A T
OR T J
WALK
"""

computer = Computer_v4()
computer.load_code("event2019/day21/input.txt")
computer.set_input_processor(ascii_input)
computer.set_output_processor(console_write)
computer.run(input=list(springscript))


answer = computer.get_output()[-1]
print("Part 1 =", answer)
assert answer == 19360724 # check with accepted answer

########
# PART 2

# J = ((!B | !C) & D & H) | !A
springscript = """NOT C J 
NOT B T
OR T J
AND D J
AND H J
NOT A T
OR T J 
RUN
"""

computer.reload_code()
computer.run(input=list(springscript))

answer = computer.get_output()[-1]
print("Part 2 =", answer)
assert answer == 1140450681 # check with accepted answer
