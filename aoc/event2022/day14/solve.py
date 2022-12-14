""" Advent of code 2022 - day 14 """
from pathlib import Path
from math import inf

########
# PART 1

SOURCE = (500, 0)

def read(filename):
    """ read the cave slice """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        horizontal_lines = {}
        vertical_lines = {}
        abs_max_y = 0
        for line in file:
            points = [tuple(map(int, path.split(','))) for path in line.strip().split(" -> ")]
            for rock_line in zip(points, points[1:]):
                (min_x, min_y), (max_x, max_y) = sorted(rock_line)

                abs_max_y = max(abs_max_y, max_y)

                if min_x - max_x == 0:
                    vertical_lines.setdefault(min_x, set()).add((min_y, max_y))
                else:
                    horizontal_lines.setdefault(min_y, set()).add((min_x, max_x))

        return (horizontal_lines, vertical_lines), abs_max_y


def is_rock(point, rock_lines) -> bool:
    """ Checks if a point is a rock """
    point_x, point_y = point

    horizontal_lines, vertical_lines = rock_lines

    if point_x in vertical_lines:
        for min_y, max_y in vertical_lines[point_x]:
            if min_y <= point_y <= max_y:
                return True

    if point_y in horizontal_lines:
        for min_x, max_x in horizontal_lines[point_y]:
            if min_x <= point_x <= max_x:
                return True

    return False


def draw(rock_lines, sand_units, from_x, to_x, from_y, to_y):
    """ Draw a specific range """
    for pos_y in range(from_y, to_y):
        print(f"{pos_y:2} ", end="")
        for pos_x in range(from_x, to_x):
            if (pos_x, pos_y) == SOURCE:
                char = '+'
            elif is_rock((pos_x, pos_y), rock_lines):
                char = '#'
            elif (pos_x, pos_y) in sand_units:
                char = 'o'
            else:
                char = '.'

            print(char, end="")
        print()


def drop_sand(rock_lines, abs_max_y, sand_units):
    """ Simulate a sand drop """
    pos_x, pos_y = SOURCE

    moved = True
    while moved:
        if pos_y == abs_max_y:
            return False

        moved = False
        for d_x, d_y in [(0, 1), (-1, 1), (1, 1)]:
            new_pos_x, new_pos_y = pos_x + d_x, pos_y + d_y

            if ((new_pos_x, new_pos_y) not in sand_units
                and not is_rock((new_pos_x, new_pos_y), rock_lines)):

                pos_x, pos_y = new_pos_x, new_pos_y
                moved = True
                break

    sand_units.add((pos_x, pos_y))

    return (pos_x, pos_y) != SOURCE


def fill_pit(rock_lines, abs_max_y):
    """ Fill the pit """
    sand_units = set()

    counter = 0
    while drop_sand(rock_lines, abs_max_y, sand_units):
        counter += 1

    #draw(rock_lines, sand_units, 480, 520, 0, 12)

    return counter


ex1 = read("example1.txt")
assert fill_pit(*ex1) == 24

inp = read("input.txt")
ANSWER = fill_pit(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 696 # check with accepted answer

########
# PART 2

def add_bottom(rock_lines, abs_max_y):
    """ Add a bottom to the rock lines """
    horizontal_lines, vertical_lines = rock_lines

    horizontal_lines.setdefault(abs_max_y + 2, set()).add((-inf, inf))

    return (horizontal_lines, vertical_lines), abs_max_y + 2


assert fill_pit(*add_bottom(*ex1)) + 1 == 93

ANSWER = fill_pit(*add_bottom(*inp)) + 1
print("Part 2 =", ANSWER)
assert ANSWER == 23610 # check with accepted answer
