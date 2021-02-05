from event2019.day13.computer_v4 import Computer_v4
import sys
import re

########
# PART 1

"""
Movement via north, south, east, or west.
To take an item the droid sees in the environment, use the command take <name of item>. For example, if the droid reports seeing a red ball, you can pick it up with take red ball.
To drop an item the droid is carrying, use the command drop <name of item>. For example, if the droid is carrying a green ball, you can drop it with drop green ball.
To get a list of all of the items the droid is currently carrying, use the command inv (for "inventory").
"""

def console_write(val):
    print(chr(val), end="")
    return chr(val)


def stdin_input(func):
    return ord(sys.stdin.read(1))


def ascii_output(val):
    return chr(val)


def ascii_input(func):
    return ord(func())


def interactive():
    computer = Computer_v4()
    computer.load_code("event2019/day25/input.txt")
    computer.set_input_processor(stdin_input)
    computer.set_output_processor(console_write)
    computer.run()

    return "".join(computer.get_output())


def scripted():
    script = """west
take semiconductor
west
take planetoid
west
take food ration
west
take fixed point
east
east
south
east
east
north
east
north
"""

    computer = Computer_v4()
    computer.load_code("event2019/day25/input.txt")
    computer.set_input_processor(ascii_input)
    computer.set_output_processor(ascii_output)
    #computer.set_output_processor(console_write)
    computer.run(input=list(script))

    return "".join(computer.get_output())


#answer = re.findall(r"You should be able to get in by typing (\d+) on the keypad at the main airlock", interactive())
answer = re.findall(r"You should be able to get in by typing (\d+) on the keypad at the main airlock", scripted())
print("Part 1 =", answer)


