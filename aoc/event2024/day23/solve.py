""" Advent of code 2024 - day 23 """

from collections import defaultdict
from itertools import combinations
from pathlib import Path

########
# PART 1


type Network = dict[str, set[str]]


def read(filename: str) -> Network:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        network = defaultdict(set)

        for line in file:
            a, b = line.strip().split('-')
            network[a].add(b)
            network[b].add(a)

        return network


def find_groups(network: Network, startswith: str):
    """ find groups of 3 """
    to_check = list(network.keys())
    loops = set()

    while to_check:
        a = to_check.pop()

        if a.startswith(startswith):
            for b, c in combinations(network[a], 2):
                if c in network[b]:
                    loops.add(tuple(sorted((a, b, c))))

    return loops


ex1 = read("example1.txt")
assert len(find_groups(ex1, "t")) == 7


inp = read("input.txt")
ANSWER = len(find_groups(inp, "t"))
print("Part 1 =", ANSWER)
assert ANSWER == 926  # check with accepted answer

########
# PART 2


def find_largest_group(network: Network):
    """ find largest group """
    to_check = [(x,) for x in network.keys()]
    checked = set()

    while to_check:
        cur = to_check.pop()

        if cur in checked:
            continue

        checked.add(cur)

        common = set(network[cur[0]])
        for n in cur[1:]:
            common = common.intersection(network[cur[1]])

        for elem in common:
            if elem not in cur and network[elem].issuperset(cur):
                n = tuple(sorted(cur + (elem,)))
                if n not in checked:
                    to_check.append(n)

    return max((len(x), x) for x in checked)[1]


assert ",".join(find_largest_group(ex1)) == "co,de,ka,ta"

ANSWER = ",".join(find_largest_group(inp))
print("Part 2 =", ANSWER)
assert ANSWER == "az,ed,hz,it,ld,nh,pc,td,ty,ux,wc,yg,zz"  # check with accepted answer
