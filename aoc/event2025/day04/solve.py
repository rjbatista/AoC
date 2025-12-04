""" Advent of code 2025 - day 04 """

from pathlib import Path

type Coord = tuple[int, int]
type Grid = set[Coord]

########
# PART 1


def read(filename: str) -> Grid:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        grid = set()
        for y, line in enumerate(file):
            for x, ch in enumerate(line):
                if ch == '@':
                    grid.add((x, y))

        return grid


def find_accessible(grid: Grid) -> int:
    """ find accessible rolls """
    possibilities = list((dx, dy) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dx != 0 or dy != 0)

    accessible = []
    for x, y in grid:
        neighbours = sum(1 if (x + dx, y + dy) in grid else 0 for (dx, dy) in possibilities)
        if neighbours < 4:
            accessible.append((x, y))

    return accessible


ex1 = read("example1.txt")
assert len(find_accessible(ex1)) == 13

inp = read("input.txt")
ANSWER = len(find_accessible(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 1435  # check with accepted answer

########
# PART 2


def remove_rolls(original_grid: Grid) -> int:
    """ Remove all the accessible rolls """
    grid = original_grid.copy()

    total = 0
    accessible = find_accessible(grid)
    while accessible:
        total += len(accessible)

        for p in accessible:
            grid.remove(p)

        accessible = find_accessible(grid)

    return total


assert remove_rolls(ex1) == 43

ANSWER = remove_rolls(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 8623  # check with accepted answer
