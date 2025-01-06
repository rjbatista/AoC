""" Advent of code 2015 - day 24 """

from itertools import combinations
from functools import reduce
from operator import mul
from pathlib import Path

########
# PART 1


def read_packages():
    """ read from file """
    with Path(__file__).parent.joinpath("input.txt").open("r", encoding="ascii") as file:
        return [int(x) for x in file.readlines()]


def find_best_combo_qe(packages, groups: int = 3):
    """ Find the smallest quantum entanglement """
    assert sum(packages) % groups == 0

    wanted_weight_per_slot = sum(packages) // groups
    package_set = set(packages)

    for size in range(1, len(packages) + 1):
        all_valid = [(x, reduce(mul, x))
                     for x in combinations(packages, size)
                     if sum(x) == wanted_weight_per_slot]

        if all_valid:
            all_valid = sorted(all_valid, key=lambda x: x[1])

            for valid in all_valid:
                # check the rest
                if groups == 1:
                    return (valid,)

                rest = find_best_combo_qe(package_set - set(valid[0]), groups - 1)

                if rest:
                    return (valid,) + rest


# example
ex1 = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
assert find_best_combo_qe(ex1)[0][1] == 99

inp = read_packages()
answer = find_best_combo_qe(inp)[0][1]
print("Part 1 =", answer)
assert answer == 11266889531  # check with accepted answer

########
# PART 2

answer = find_best_combo_qe(inp, 4)[0][1]
print("Part 2 =", answer)
assert answer == 77387711  # check with accepted answer
