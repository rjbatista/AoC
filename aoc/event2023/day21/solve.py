""" Advent of code 2023 - day 21 """
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
type GardenMap = tuple[int, int, set[Coord]]

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def read(filename: str) -> tuple[GardenMap, Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        rocks = set()
        max_x, max_y = 0, 0
        for y, line in enumerate(file):
            max_y = max(max_y, y)
            for x, ch in enumerate(line.strip()):
                max_x = max(max_x, x)
                if ch == '#':
                    rocks.add((x, y))
                elif ch == 'S':
                    start = (x, y)

        return (max_x + 1, max_y + 1, rocks), start


def print_garden(garden_map: GardenMap, positions: set[Coord]) -> None:
    """ Print the garden """
    width, height, rocks = garden_map

    for y in range(height):
        for x in range(width):
            if (x, y) in positions:
                print('O', end="")
            else:
                print('#' if (x, y) in rocks else '.', end="")
        print()


def find_reach(garden_map: GardenMap, position: Coord, moves: int) -> int:
    """ Find the possible reach with the available steps """

    width, height, rocks = garden_map
    todo = set([position])
    for _ in range(moves):
        new_todo = set()
        for (x, y) in todo:
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy

                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in rocks:
                    new_todo.add((nx, ny))

        todo = new_todo

    # print_garden(garden_map, todo)

    return len(todo)


ex1 = read("example1.txt")
assert find_reach(*ex1, 6) == 16

inp = read("input.txt")
ANSWER = find_reach(*inp, 64)
print("Part 1 =", ANSWER)
assert ANSWER == 3615  # check with accepted answer

########
# PART 2

# looking at the input, it's a diamond shape, moving in all directions
# starting in the middle with no obstacles in the directions,
# reaching the borders at 65 moves (131 (size) // 2) and
# then the other borders of the infinite repetition after 131 moves
#
# 26501365 is exactly 65 + 131 * 202300, so not in a "in the middle of a thing" status

# the area of the covered surface would be the area of the diamond,
# but since there are gaps, we can figure out the polinomial for the area
# by solving for 3 specific values, considering only "full moves"
# f(x) = a*x^2 + b*x + c, for x=[0 (65 moves), 1 (65 + 131 moves), 2 (65 + 131*2 moves)]


# pylint: disable=too-many-locals
def find_reach_2(garden_map: GardenMap, position: Coord, moves: list[int]) -> list[int]:
    """ Find the possible reach with the available steps, in a infinite plane """

    width, height, rocks = garden_map
    todo = set([position])
    results = []
    for i in range(max(moves) + 1):
        if i == moves[0]:
            moves.pop(0)
            results.append(len(todo))

        new_todo = set()
        for x, y in todo:
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy

                if (nx % width, ny % height) not in rocks:
                    new_todo.add((nx, ny))

        todo = new_todo

    return results


def find_area_formula(f: list[int], moves: int):
    """ Solve the equation for the specified moves and results """

    # consider only the full moves and not steps, so
    # f(0) = 0**2 * a + 0 * b + * c = c
    # f(1) = 1**2 * a + 1 * b + c   = a + b + c
    # f(2) = 2**2 * a + 2 * b       = 4 * a + 2 * b + c

    # determine the coefficients
    c = f[0]
    # cutting a: f(2) - 4 * f(1) = - 2 * b - 3 * f(0) <=> b = (4 * f(1) - f(2) - 3 * c) // 2
    b = (4 * f[1] - f[2] - 3 * c) // 2
    # replacing for a
    a = f[1] - b - c

    wanted_full_moves = (moves - 65) // 131

    return a * wanted_full_moves**2 + b * wanted_full_moves + c


ANSWER = find_area_formula(find_reach_2(*inp, [65, 65 + 131, 65 + (131 * 2)]), 26501365)
print("Part 2 =", ANSWER)
assert ANSWER == 602259568764234  # check with accepted answer
