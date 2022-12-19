""" Advent of code 2022 - day 18 """
from pathlib import Path
from math import inf
import heapq

########
# PART 1

POSSIBLE_MOVES = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

def read(filename: str) -> list:
    """ Read the commands """
    cubes = set()
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        for line in file:
            cubes.add(tuple(map(int, line.strip().split(","))))

    return cubes


def count_faces(cubes):
    """ Count the exposed faces """
    faces = 0

    for cube in cubes:
        for axis in POSSIBLE_MOVES:
            if tuple(map(sum, zip(cube, axis))) not in cubes:
                faces += 1

    return faces


ex1 = read("example1.txt")
assert count_faces(ex1) == 64

inp = read("input.txt")

ANSWER = count_faces(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 3432 # check with accepted answer

########
# PART 2

def flood_fill(cubes, dimensions):
    """ Flood fill to find the relevant outside """
    min_x, max_x, min_y, max_y, min_z, max_z = dimensions

    todo = [(min_x, min_y, min_z)]
    heapq.heapify(todo)

    outside = set(todo)
    while todo:
        pos_x, pos_y, pos_z = heapq.heappop(todo)

        for d_x, d_y, d_z in POSSIBLE_MOVES:
            new_pos_x = pos_x + d_x
            new_pos_y = pos_y + d_y
            new_pos_z = pos_z + d_z

            if (min_x <= new_pos_x <= max_x and
                min_y <= new_pos_y <= max_y and
                min_z <= new_pos_z <= max_z):

                if ((new_pos_x, new_pos_y, new_pos_z) not in cubes
                    and (new_pos_x, new_pos_y, new_pos_z) not in outside):

                    outside.add((new_pos_x, new_pos_y, new_pos_z))
                    heapq.heappush(todo, (new_pos_x, new_pos_y, new_pos_z))

    return outside


def count_faces_without_pockets(cubes):
    """ Count the exposed faces """
    faces = 0

    min_x = min_y = min_z = inf
    max_x = max_y = max_z = -inf
    for pos_x, pos_y, pos_z in cubes:
        min_x = min(min_x, pos_x)
        max_x = max(max_x, pos_x)
        min_y = min(min_y, pos_y)
        max_y = max(max_y, pos_y)
        min_z = min(min_z, pos_z)
        max_z = max(max_z, pos_z)
    dimensions = (min_x - 1, max_x + 1, min_y - 1, max_y + 1, min_z - 1, max_z + 1)

    outside = flood_fill(cubes, dimensions)

    for cube in cubes:
        for axis in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
            possibility = tuple(map(sum, zip(cube, axis)))
            if possibility not in cubes and possibility in outside:
                faces += 1

    return faces


assert count_faces_without_pockets(ex1) == 58

ANSWER = count_faces_without_pockets(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 2042 # check with accepted answer
