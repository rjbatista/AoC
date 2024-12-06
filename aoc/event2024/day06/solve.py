""" Advent of code 2024 - day 06 """

from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
type Guard = tuple[Coord, Coord]
type Lab = tuple[Coord, dict[Coord, str]]


def read(filename: str) -> tuple[Lab, Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        floorplan = {}
        guard = None
        w, h = 0, 0
        for y, line in enumerate(file):
            h = y
            for x, ch in enumerate(line.strip()):
                w = x
                if ch == '^':
                    guard = (x, y), (0, -1)
                elif ch != '.':
                    floorplan[(x, y)] = ch

        return (floorplan, (w, h)), guard


def patrol(lab: Lab, guard: Coord, check_cycle: bool = False) -> int:
    """ Count all the visited positions of the guard """
    visited = set()
    visited_loop = set()

    floorplan, (w, h) = lab

    (x, y), (dx, dy) = guard
    while 0 <= x <= w and 0 <= y <= h:
        nx, ny = x + dx, y + dy

        visited.add((x, y))

        if check_cycle:
            if (x, y, dx, dy) in visited_loop:
                return visited, True

            visited_loop.add((x, y, dx, dy))

        if floorplan.get((nx, ny), None):
            # turn 90 degrees clockwise
            dx, dy = -dy, dx

            continue

        x, y = nx, ny

    return visited, False


ex1 = read("example1.txt")
assert len(patrol(*ex1)[0]) == 41

inp = read("input.txt")
ANSWER = len(patrol(*inp)[0])
print("Part 1 =", ANSWER)
assert ANSWER == 5162  # check with accepted answer

########
# PART 2


def find_possible_obstructions(lab: Lab, guard: Coord) -> int:
    """ Find all the possible obstructions for the guard """

    passed = set()
    obstacles = set()

    floorplan, (w, h) = lab

    (x, y), (dx, dy) = guard
    while 0 <= x <= w and 0 <= y <= h:
        nx, ny = x + dx, y + dy

        passed.add((x, y))

        if floorplan.get((nx, ny), None):
            # turn
            dx, dy = -dy, dx

            continue

        if 0 <= nx <= w and 0 <= ny <= h and (nx, ny) not in passed:
            if patrol(({**floorplan, (nx, ny): 'O'}, (w, h)), ((x, y), (dx, dy)), True)[1]:
                if (nx, ny) not in floorplan:
                    obstacles.add((nx, ny))

        x, y = nx, ny

    return len(obstacles)


assert find_possible_obstructions(*ex1) == 6

ex2 = read("example2.txt")
assert find_possible_obstructions(*ex2) == 2

ANSWER = find_possible_obstructions(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 1909  # check with accepted answer
