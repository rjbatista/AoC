""" Advent of code 2024 - day 01 """

from pathlib import Path
from collections import Counter

########
# PART 1

type IdList = list[int]


def read(filename: str) -> tuple[IdList, IdList]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return tuple(
            zip(*(map(int, line.split()) for line in file))
        )


def pair_and_distance(list1: IdList, list2: IdList) -> int:
    """ Pair lists and calculate distances """

    return sum(abs(x - y) for x, y in zip(sorted(list1), sorted(list2)))


ex1 = read("example1.txt")
assert pair_and_distance(*ex1) == 11

inp = read("input.txt")
ANSWER = pair_and_distance(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 2086478  # check with accepted answer

########
# PART 2


def calc_similarity_score(list1: IdList, list2: IdList) -> int:
    """ Calculate the similarity score for the given lists """
    counts = Counter(list2)

    return sum(x * counts[x] for x in list1)


assert calc_similarity_score(*ex1) == 31

ANSWER = calc_similarity_score(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 24941624  # check with accepted answer
