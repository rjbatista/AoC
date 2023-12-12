""" Advent of code 2023 - day 08 """
from functools import reduce
from itertools import cycle
from math import gcd
from pathlib import Path
import re

########
# PART 1

type Node = tuple[str, str]
type Network = tuple[list[int], dict[str, Node]]


def read(filename: str) -> Network:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        instructions = [0 if ch == 'L' else 1 for ch in file.readline().strip()]
        file.readline()

        node_expr = re.compile(r'(\w+) = \((\w+), (\w+)\)')
        nodes = {}

        for line in file:
            node, left, right = node_expr.match(line).groups()

            nodes[node] = (left, right)

        return instructions, nodes


def find(what: str, network: Network, starting: str = 'AAA') -> int:
    """ Find the number of steps to a node in the network """

    step = 0
    instructions, nodes = network

    instructions = cycle(instructions)

    current = starting
    while current[2] != what[2]:
        step += 1

        current_node = nodes[current]
        current = current_node[next(instructions)]

    return step


ex1 = read("example1.txt")
assert find('ZZZ', ex1) == 2

ex2 = read("example2.txt")
assert find('ZZZ', ex2) == 6


inp = read("input.txt")
ANSWER = find('ZZZ', inp)
print("Part 1 =", ANSWER)
assert ANSWER == 15989  # check with accepted answer

########
# PART 2


def get_starting_nodes(network: Network):
    """ Get the starting nodes """
    _, nodes = network

    return [x for x in nodes.keys() if x.endswith('A')]


def find_for_all(network: Network) -> int:
    """ Find all simultaneously """

    starting_nodes = get_starting_nodes(network)

    # find the distances to objective separately
    distances = sorted([find('ZZZ', network, start) for start in starting_nodes], reverse=True)

    # get the common denominator
    dist_gcd = gcd(*distances)

    # get the rotations necessary for each objective, to get the factor necessary for a match
    rotations = reduce(lambda x, y: x * y, [x // dist_gcd for x in distances])

    # return the total steps necessary
    return rotations * dist_gcd


ex3 = read("example3.txt")
assert find_for_all(ex3) == 6

ANSWER = find_for_all(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 13830919117339  # check with accepted answer
