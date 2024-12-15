""" Advent of code 2024 - day 14 """

from collections import Counter
from itertools import count
from math import inf, log, prod
from pathlib import Path
import re

########
# PART 1

type Coord = tuple[int, int]
type Robot = tuple[Coord, Coord]


def read(filename: str) -> list[Robot]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        pattern = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")

        robots = []
        for line in file:
            x, y, vx, vy = map(int, pattern.match(line).groups())
            robots.append(((x, y), (vx, vy)))

        return robots


def simulate(robots: list[Robot], seconds: int, width=101, height=103) -> list[Robot]:
    new_robots = []
    for (x, y), (vx, vy) in robots:
        new_robots.append((((x + vx * seconds) % width, (y + vy * seconds) % height), (vx, vy)))

    return new_robots


def print_map(robots: list[Robot], width=101, height=103) -> list[Robot]:
    robots_by_pos = Counter(p for p, _ in robots)

    for y in range(height):
        for x in range(width):
            robots_here = robots_by_pos.get((x, y))

            print(robots_here if robots_here else '.', end="")
        print()
    print()


def get_quadrants(robots: list[Robot], width=101, height=103) -> int:
    middle_w, middle_h = width // 2, height // 2

    quadrants = [0] * 4
    for (x, y), _ in robots:
        if x != middle_w and y != middle_h:
            p = 0 if x < middle_w else 1
            p += 0 if y < middle_h else 2
            quadrants[p] += 1

    return quadrants


ex1 = read("example1.txt")
assert prod(get_quadrants(simulate(ex1, 100, 11, 7), 11, 7)) == 12

inp = read("input.txt")
ANSWER = prod(get_quadrants(simulate(inp, 100)))
print("Part 1 =", ANSWER)
assert ANSWER == 228457125  # check with accepted answer

########
# PART 2


def calculate_entropy(points: list[int], max: int):
    """ Calculates the entropy for the set of points """
    ent = 0.0
    counts = Counter(points)

    size = float(max)
    for x in range(max):
        freq = counts[x]
        if freq > 0:
            freq = float(freq) / size
            ent = ent + freq * log(freq, 2)

    return -ent


def simulate_till_easter_egg(robots: list[Robot], width=101, height=103) -> list[Robot]:
    """ simulate to find the easter egg """
    min_x = inf, inf
    min_y = inf, inf

    for sec in range(max(width, height)):
        new_robots = simulate(robots, sec, width, height)

        if sec < width:
            ent = calculate_entropy([x for (x, _), _ in new_robots], width)

        # calculate the distribuition of x with lowest entropy (most likely an image and not random)
        min_x = min(min_x, (ent, sec))

        if sec < height:
            ent = calculate_entropy([y for (_, y), _ in new_robots], height)

        # calculate the distribuition of y with lowest entropy (most likely an image and not random)
        min_y = min(min_y, (ent, sec))

    _, min_x = min_x
    _, min_y = min_y

    # find match for the wanted entropy on x and y (Chinese Remainder Theorem)
    space = width * height
    for iteration in count():
        value = (min_x + width * iteration) % space

        if value == (min_y + height * iteration) % space:
            break

    return value


ANSWER = simulate_till_easter_egg(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 6493  # check with accepted answer

# print_map(simulate(inp, ANSWER))
