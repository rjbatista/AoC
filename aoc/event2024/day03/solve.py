""" Advent of code 2024 - day 03 """

from pathlib import Path
import re

########
# PART 1

type Mul = tuple[int, int]

def read(filename: str) -> list[Mul]:
    """ Read from a file """

    return Path(__file__).parent.joinpath(filename).read_text()


def get_muls(s: str) -> list[Mul]:
    """ Get the valid multiplications from the string """

    p = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    return [(int(x), int (y)) for x, y in p.findall(s)]


def sum_muls(muls: list[Mul]) -> int:
    """ Sum the results from all the multiplications """
    return sum(x * y for x, y in muls)


ex1 = read("example1.txt")
assert sum_muls(get_muls(ex1)) == 161

inp = read("input.txt")

ANSWER = sum_muls(get_muls(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 179571322  # check with accepted answer

########
# PART 2

def get_muls_with_conditionals(s: str) -> list[Mul]:
    """ Get the valid multiplications from the string """

    p = re.compile(r"(?:(mul)\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\))")

    active = True
    muls = []
    for mul, x, y, do, dont in p.findall(s):
        if do:
            active = True
        elif dont:
            active = False
        elif mul and active:
            muls.append((int(x), int(y)))

    return muls


ex2 = read("example2.txt")
assert sum_muls(get_muls_with_conditionals(ex2)) == 48

ANSWER = sum_muls(get_muls_with_conditionals(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 103811193  # check with accepted answer
