""" Advent of code 2024 - day 19 """

import functools
from pathlib import Path

########
# PART 1


def read(filename: str) -> tuple[list[str], list[str]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        available = set(file.readline().strip().split(', '))
        file.readline()
        wanted_list = [line.strip() for line in file]

        return available, wanted_list


def count_possible(available: set[str], wanted_list: str) -> bool:
    """ Check if a combination is possible """
    @functools.cache
    def _is_possible(wanted):
        for have in available:
            if wanted.startswith(have):
                todo = wanted[len(have):]

                if not todo or _is_possible(todo):
                    return True

        return False

    return sum(1 for wanted in wanted_list if _is_possible(wanted))


ex1 = read("example1.txt")
assert count_possible(*ex1) == 6

inp = read("input.txt")
ANSWER = count_possible(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 280  # check with accepted answer

########
# PART 2


def count_all(available: set[str], wanted_list: str) -> bool:
    """ Count all possible """
    @functools.cache
    def _count_all(wanted) -> int:
        count = 0
        for have in available:
            if wanted.startswith(have):
                todo = wanted[len(have):]

                if todo:
                    count += _count_all(todo)
                else:
                    count += 1

        return count

    return sum(_count_all(wanted) for wanted in wanted_list)


assert count_all(*ex1) == 16

ANSWER = count_all(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 606411968721181  # check with accepted answer
