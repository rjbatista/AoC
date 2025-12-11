""" Advent of code 2025 - day 08 """

from itertools import combinations
from math import inf, prod, sqrt
from pathlib import Path
from typing import Iterator

########
# PART 1

type Coord = tuple[int, int, int]


def read(filename: str) -> list[Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [tuple(map(int, line.split(','))) for line in file]


def calc_distances(boxes: list[Coord]) -> Iterator[tuple[Coord, Coord]]:
    """ calculate the distances"""
    def dist(p1: Coord, p2: Coord) -> float:
        return sqrt(sum((p - q)**2 for p, q in zip(p1, p2)))

    return ((a, b) for _, a, b in
            sorted((dist(box1, box2), box1, box2) for box1, box2 in combinations(boxes, 2)))


def connect_closest(boxes: list[Coord], n: int) -> list[list[Coord]]:
    """ connect the closest n boxes in circuits """

    all_pairs = calc_distances(boxes)
    circuits = [[x] for x in boxes]
    box_circuit = {x: i for (i, x) in enumerate(boxes)}
    total_circuits = len(boxes)

    while n:
        if n != inf:
            n -= 1

        box1, box2 = next(all_pairs)
        box_circuit1 = box_circuit[box1]
        box_circuit2 = box_circuit[box2]

        if box_circuit1 == box_circuit2:
            # do nothing
            continue

        # connect circuits
        for box in circuits[box_circuit2]:
            box_circuit[box] = box_circuit1

        circuits[box_circuit1] += circuits[box_circuit2]
        circuits[box_circuit2] = []
        total_circuits -= 1

        if total_circuits == 1:
            # special case, return the prod of X of the 2 boxes
            # a bit of an hack....
            return box1[0] * box2[0]

    return circuits


def print_circuits(circuits: list[list[Coord]]):
    """ print the circuits """
    for idx, circuit in enumerate(circuits):
        print(idx, "------\t", circuit)


ex1 = read("example1.txt")
assert prod(sorted((len(x) for x in connect_closest(ex1, 10)), reverse=True)[0:3]) == 40

inp = read("input.txt")
ANSWER = prod(sorted((len(x) for x in connect_closest(inp, 1000)), reverse=True)[0:3])
print("Part 1 =", ANSWER)
assert ANSWER == 57970  # check with accepted answer

########
# PART 2

assert connect_closest(ex1, inf) == 25272

ANSWER = connect_closest(inp, inf)
print("Part 2 =", ANSWER)
assert ANSWER == 8520040659  # check with accepted answer
