""" Advent of code 2025 - day 06 """

from math import prod
from pathlib import Path
import itertools

########
# PART 1


OP = {
    '+': sum,
    '*': prod
}


def read(filename: str) -> tuple[list[list[int]], list[str]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        lines = []
        for line in file:
            lines.append(line.split())

        return list(list(map(int, line)) for line in lines[:-1]), lines[-1]


def execute(numbers: list[int], operations: list[str]) -> int:
    """ execute the operations on the numbers """
    total = 0
    for idx, column in enumerate(zip(*numbers)):
        total += OP[operations[idx]](column)

    return total


ex1 = read("example1.txt")
assert execute(*ex1) == 4277556

inp = read("input.txt")
ANSWER = execute(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 4580995422905  # check with accepted answer

########
# PART 2


def read_rtl(filename: str) -> tuple[list[list[int]], list[str]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        lines = [line[:-1] for line in file]

        column = list(''.join(x).strip() for x in zip(*lines[:-1]))
        numbers = [list(map(int, y))
                   for x, y in itertools.groupby(column, lambda z: z == '') if not x]

        return numbers, lines[-1].split()


def execute_rtl(numbers: list[int], operations: list[str]) -> int:
    """ execute the operations on the numbers """
    total = 0
    for idx, column in enumerate(numbers):
        total += OP[operations[idx]](column)

    return total


ex1 = read_rtl("example1.txt")
assert execute_rtl(*ex1) == 3263827

inp = read_rtl("input.txt")
ANSWER = execute_rtl(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 10875057285868  # check with accepted answer
