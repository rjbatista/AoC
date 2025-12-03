""" Advent of code 2025 - day 01 """

########
# PART 1

from pathlib import Path
from typing import Iterator


def read(filename: str) -> Iterator[int]:
    """ Read from a file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        for line in file:
            match line[0]:
                case 'R':
                    yield int(line[1:])
                case 'L':
                    yield -int(line[1:])
                case _:
                    raise ValueError(f"Invalid line: {line}")


def count_zeros_on_stop(rotations: Iterator[int], start=50):
    """ Count times dial stays at zero """
    dial = start
    counter = 0

    for rotation in rotations:
        dial = (dial + rotation) % 100

        if dial == 0:
            counter += 1

    return counter


example1 = list(read("example1.txt"))

assert count_zeros_on_stop(example1) == 3

inp = list(read("input.txt"))
ANSWER = count_zeros_on_stop(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 964  # check with accepted answer

########
# PART 2


def count_zeros_on_rotation(rotations: Iterator[int], start=50):
    """ Count times dial passes at zero """
    dial = start
    counter = 0

    for rotation in rotations:
        odial = dial

        # remove extra rotations
        extras = (abs(rotation) // 100) * (rotation // abs(rotation))
        rotation = rotation - (extras * 100)
        counter += abs(extras)

        dial = dial + rotation

        if dial % 100 != 0:
            extras = abs(dial) // 100
            counter += extras

        dial = dial % (-100 if dial < 0 else 100)

        if dial == 0 or dial * odial < 0:
            counter += 1

    return counter


assert count_zeros_on_rotation(example1) == 6

ANSWER = count_zeros_on_rotation(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 5872  # check with accepted answer
