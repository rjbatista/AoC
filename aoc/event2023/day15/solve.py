""" Advent of code 2023 - day 15 """
from collections import OrderedDict
from functools import reduce
from pathlib import Path

########
# PART 1


def read(filename: str) -> list[str]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return file.readline().strip().split(',')


def hash_value(s: str) -> int:
    """ Holiday ASCII String Helper algorithm """
    return reduce(lambda x, y: ((x + ord(y)) * 17) & 0xFF, s, 0)


assert hash_value("HASH") == 52

ex1 = read("example1.txt")
assert sum(hash_value(s) for s in ex1) == 1320

inp = read("input.txt")
ANSWER = sum(hash_value(s) for s in inp)
print("Part 1 =", ANSWER)
assert ANSWER == 516657  # check with accepted answer

########
# PART 2


def calculate_focusing_power(instructions: list[str]) -> int:
    """ Calculate the focusing power after organizing the boxes with the specified instructions """

    boxes = {}
    for instr in instructions:
        if '=' in instr:
            label, focal_length = instr.split("=")
            box = hash_value(label)

            if box not in boxes:
                boxes[box] = OrderedDict()

            boxes[box][label] = int(focal_length)
        else:
            label = instr[:-1]
            box = hash_value(label)

            if box in boxes and label in boxes[box]:
                del boxes[box][label]

    return sum((no + 1) * pos * value
               for no, values in boxes.items()
               for pos, value in enumerate(values.values(), 1))


assert calculate_focusing_power(ex1) == 145

ANSWER = calculate_focusing_power(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 210906  # check with accepted answer
