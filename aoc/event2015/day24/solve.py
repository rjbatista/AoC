from itertools import combinations
from functools import reduce
from operator import mul

########
# PART 1

def read_packages():
    with open("event2015/day24/input.txt") as f:
        return [int(x) for x in f.readlines()]


def findbestcombo_qe(packages, groups = 3):
    assert sum(packages) % groups == 0

    wanted_weight_per_slot = sum(packages) // groups
    package_set = set(packages)

    for size in range(1, len(packages) + 1):
        all_valid = [(x, reduce(mul, x)) for x in combinations(packages, size) if sum(x) == wanted_weight_per_slot]

        if all_valid:
            all_valid = sorted(all_valid, key = lambda x : x[1])

            for valid in all_valid:
                # check the rest
                if groups == 1:
                    return (valid,)
                else:
                    rest = findbestcombo_qe(package_set - set(valid[0]), groups - 1)

                    if rest:
                        return (valid,) + rest


# example
packages = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
findbestcombo_qe(packages)[0][1] == 90

packages = read_packages()
answer = findbestcombo_qe(packages)[0][1]
print("Part 1 =", answer)
assert answer == 11266889531 # check with accepted answer

########
# PART 2

answer = findbestcombo_qe(packages, 4)[0][1]
print("Part 2 =", answer)
assert answer == 77387711 # check with accepted answer
