""" Advent of code 2023 - day 09 """
from pathlib import Path

########
# PART 1


def read(filename: str) -> list[list[int]]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [list(map(int, line.split())) for line in file]


def differences(sequence: list[int]) -> list[int]:
    """ Get the difference list """
    return [y - x for (x, y) in zip(sequence, sequence[1:])]


def extrapolate(sequence: list[int]) -> int:
    """ Extrapolate the next value """

    diff = differences(sequence)

    return sequence[-1] if all(x == 0 for x in diff) else sequence[-1] + extrapolate(diff)


ex1 = read("example1.txt")
assert sum(extrapolate(seq) for seq in ex1) == 114

inp = read("input.txt")
ANSWER = sum(extrapolate(seq) for seq in inp)
print("Part 1 =", ANSWER)
assert ANSWER == 2101499000  # check with accepted answer

########
# PART 2


def extrapolate_backwards(sequence: list[int]) -> int:
    """ Extrapolate the next value """

    diff = differences(sequence)

    return sequence[0] if all(x == 0 for x in diff) else sequence[0] - extrapolate_backwards(diff)


assert sum(extrapolate_backwards(seq) for seq in ex1) == 2

ANSWER = sum(extrapolate_backwards(seq) for seq in inp)
print("Part 2 =", ANSWER)
assert ANSWER == 1089  # check with accepted answer
