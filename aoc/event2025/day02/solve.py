""" Advent of code 2025 - day 02 """

from pathlib import Path
import re

########
# PART 1


def read(filename: str) -> list[tuple[int, int]]:
    """ Read from a file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [tuple(map(int, x.split("-"))) for x in file.readline().split(",")]


def find_invalid_id_repeat_twice(start: int, end: int):
    """ find the invalid ids in the range """

    ret = []
    p = re.compile(r"^(\d+)\1$")
    for i in range(start, end + 1):
        if p.match(str(i)):
            ret.append(i)

    return ret


ex1 = read("example1.txt")

assert (sum(sum(y) for y in (find_invalid_id_repeat_twice(*x) for x in ex1))) == 1227775554

inp = read("input.txt")

ANSWER = sum(sum(y) for y in (find_invalid_id_repeat_twice(*x) for x in inp))
print("Part 1 =", ANSWER)
assert ANSWER == 20223751480  # check with accepted answer

########
# PART 2


def find_invalid_id_repeat_any(start: int, end: int):
    """ find the invalid ids in the range """

    ret = []
    p = re.compile(r"^(\d+)\1+$")
    for i in range(start, end + 1):
        if p.match(str(i)):
            ret.append(i)

    return ret


assert (sum(sum(y) for y in (find_invalid_id_repeat_any(*x) for x in ex1))) == 4174379265


ANSWER = sum(sum(y) for y in (find_invalid_id_repeat_any(*x) for x in inp))
print("Part 2 =", ANSWER)
assert ANSWER == 30260171216  # check with accepted answer
