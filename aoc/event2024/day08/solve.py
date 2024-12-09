""" Advent of code 2024 - day 08 """

from collections import defaultdict
from itertools import combinations, count
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
type Antennas = dict[str, list[Coord]]


def read(filename: str) -> tuple[Antennas, Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        antennas = defaultdict(list)
        w, h = 0, 0
        for y, line in enumerate(file):
            h = y
            for x, ch in enumerate(line.strip()):
                w = x
                if ch != '.':
                    antennas[ch].append((x, y))

        return antennas, (w + 1, h + 1)


def find_antinodes(antennas: Antennas, size: Coord) -> int:
    """ find the antinodes for the antennas """
    antinodes = set()

    w, h = size
    for _, antenna in antennas.items():
        for (x0, y0), (x1, y1) in combinations(antenna, 2):
            dx, dy = x1 - x0, y1 - y0

            for i in [-1, 2]:
                nx, ny = x0 + i * dx, y0 + i * dy

                if 0 <= nx < w and 0 <= ny < h:
                    antinodes.add((nx, ny))

    return antinodes


ex1 = read("example1.txt")
assert len(find_antinodes(*ex1)) == 14

inp = read("input.txt")
ANSWER = len(find_antinodes(*inp))
print("Part 1 =", ANSWER)
assert ANSWER == 379  # check with accepted answer

########
# PART 2


def find_antinodes_with_resonance(antennas: Antennas, size: Coord) -> int:
    """ find the antinodes for the antennas """
    antinodes = set()

    w, h = size
    for _, antenna in antennas.items():
        for (x0, y0), (x1, y1) in combinations(antenna, 2):
            dx, dy = x1 - x0, y1 - y0

            for i in count(0):
                cont = False

                nx, ny = x0 + i * dx, y0 + i * dy
                if 0 <= nx < w and 0 <= ny < h:
                    cont = True
                    antinodes.add((nx, ny))

                nx, ny = x0 - i * dx, y0 - i * dy
                if 0 <= nx < w and 0 <= ny < h:
                    cont = True
                    antinodes.add((nx, ny))

                if not cont:
                    break

    return antinodes


assert len(find_antinodes_with_resonance(*ex1)) == 34

ex3 = read("example3.txt")
assert len(find_antinodes_with_resonance(*ex3)) == 9

ANSWER = len(find_antinodes_with_resonance(*inp))
print("Part 2 =", ANSWER)
assert ANSWER == 1339  # check with accepted answer
