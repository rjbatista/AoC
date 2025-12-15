""" Advent of code 2025 - day 09 """

from itertools import combinations
from math import prod
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]


def read(filename: str) -> list[Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return list(tuple(map(int, line.split(','))) for line in file)


def find_largest_rectangle(red_tiles: list[Coord]) -> int:
    """ find the largest rectangle """
    largest = 0
    for p1, p2 in combinations(red_tiles, 2):
        largest = max(largest, prod(1 + abs(a - b) for a, b in zip(p1, p2)))

    return largest


ex1 = read("example1.txt")
assert find_largest_rectangle(ex1) == 50

inp = read("input.txt")
ANSWER = find_largest_rectangle(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 4769758290  # check with accepted answer

########
# PART 2


def find_largest_rectangle_inside(red_tiles: list[Coord]) -> int:
    """ find the largest rectangle inside the polygon """

    def is_vertical(p1: Coord, p2: Coord):
        return p1[0] - p2[0] == 0

    def is_inside(rectangle_segments) -> bool:
        # check for intersections
        for p1, p2 in rectangle_segments:
            if is_vertical(p1, p2):
                rect_x = p1[0]
                rect_y1, rect_y2 = sorted((p1[1], p2[1]))

                for poly_segment in poly_horiz:
                    poly_y = poly_segment[0][1]
                    poly_x1, poly_x2 = sorted((poly_segment[0][0], poly_segment[1][0]))

                    if rect_y1 < poly_y < rect_y2 and poly_x1 <= rect_x <= poly_x2:
                        # intersects, hence false
                        return False
            else:
                rect_y = p1[1]
                rect_x1, rect_x2 = sorted((p1[0], p2[0]))

                for poly_segment in poly_vert:
                    poly_x = poly_segment[0][0]
                    poly_y1, poly_y2 = sorted((poly_segment[0][1], poly_segment[1][1]))

                    if rect_x1 < poly_x < rect_x2 and poly_y1 <= rect_y <= poly_y2:
                        # intersects, hence false
                        return False

        return True

    def shrink(a: int, b: int) -> tuple[int, int]:
        return min(a, b) + 1, max(a, b) - 1

    # find the segments of the polygon
    poly_segments = list(zip(red_tiles, red_tiles[1:] + red_tiles[:1]))
    poly_vert, poly_horiz = [], []
    for s in poly_segments:
        if is_vertical(*s):
            poly_vert.append(s)
        else:
            poly_horiz.append(s)

    # generate the largest rectangles
    rectangles = sorted(((p1, p2) for p1, p2 in combinations(red_tiles, 2)),
                        key=lambda x: prod(1 + abs(a - b) for a, b in zip(x[0], x[1])),
                        reverse=True)

    # get the rectangle segments
    for (x0, y0), (x1, y1) in rectangles:
        rectangle_vertexes = [(x, y) for x in shrink(x0, x1) for y in shrink(y0, y1)]
        rectangle_segments = list(zip(rectangle_vertexes,
                                      rectangle_vertexes[1:] + rectangle_vertexes[:1]))

        if not is_inside(rectangle_segments):
            continue

        return (1 + abs(x0 - x1)) * (1 + abs(y0 - y1))


assert find_largest_rectangle_inside(ex1) == 24

ANSWER = find_largest_rectangle_inside(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 1588990708  # check with accepted answer
