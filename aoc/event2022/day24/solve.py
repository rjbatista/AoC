""" Advent of code 2022 - day 24 """
from pathlib import Path
from itertools import chain
import heapq

########
# PART 1


DIRECTIONS = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1)
}

DIRECTION_SYMBOLS = dict([reversed(i) for i in DIRECTIONS.items()])


def read(filename: str) -> set:
    path = Path(__file__).parent.joinpath(filename)
    with path.open("r", encoding="ascii") as file:
        valley = {}
        max_x = 0
        max_y = 0
        for y, line in enumerate(file):
            max_y = y
            for x, char in enumerate(line):
                max_x = max(max_x, x)
                if char in DIRECTIONS:
                    valley[(x, y)] = DIRECTIONS[char]

        return valley, max_x, max_y


def valley_at_time(valley: set, max_x: int, max_y: int, t: int):
    valley_at_t = set()
    for (x, y), (dx, dy) in valley.items():
        x_at_t = (((x - 1) + dx * t) % (max_x - 2)) + 1
        y_at_t = (((y - 1) + dy * t) % (max_y - 1)) + 1

        valley_at_t.add((x_at_t, y_at_t))

    return valley_at_t, max_x, max_y


def draw_valley(valley: dict, max_x, max_y, expedition_pos):
    print("#", "#" * (max_x - 2))
    for y in range(1, max_y):
        print("#", end="")
        for x in range(1, max_x - 1):
            if expedition_pos == (x, y):
                print('E', end="")
            else:
                if (x, y) in valley:
                    print("*", end="")
                else:
                    print('.', end="")
        print("#")
    print("#" * (max_x - 2), "#")
    print()


def find_fastest_way(valley: dict, max_x, max_y):
    return _find_fastest_way(valley, max_x, max_y,
                             (1, 0), (max_x - 2, max_y), 0)


def _find_fastest_way(valley: dict, max_x, max_y, start, wanted, step):
    cycle_size = (max_x - 2) * (max_y - 1)
    todo = [(step, start)]
    heapq.heapify(todo)
    valleys = {}
    visited = set()
    visited.add((step, *start))
    while todo:
        steps, (x, y) = heapq.heappop(todo)

        if (steps + 1) % cycle_size not in valleys:
            valleys[(steps + 1) % cycle_size] = valley_at_time(
                    valley, max_x, max_y, steps + 1)

        valley_now = valleys[(steps + 1) % cycle_size]
        for dx, dy in chain(DIRECTIONS.values(), [(0, 0)]):
            nx, ny = x + dx, y + dy

            if (nx, ny) == wanted:
                return steps + 1

            if 0 < nx < max_x - 1 and 0 <= ny <= max_y:
                if (ny == 0 and nx != 1) or (ny == max_y and nx != max_x - 2):
                    continue
                if ((nx, ny) not in valley_now[0]
                   and ((steps + 1) % cycle_size, nx, ny) not in visited):

                    visited.add(((steps + 1) % cycle_size, nx, ny))
                    heapq.heappush(todo, (steps + 1, (nx, ny)))


# ex1 = read("example1.txt")

ex2 = read("example2.txt")
assert find_fastest_way(*ex2) == 18

inp = read("input.txt")
ANSWER = find_fastest_way(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 314  # check with accepted answer


########
# PART 2


def find_fastest_way_p2(valley: dict, max_x, max_y):
    steps = 0
    pos = (1, 0), (max_x - 2, max_y)
    steps = _find_fastest_way(valley, max_x, max_y, *pos, steps)
    steps = _find_fastest_way(valley, max_x, max_y, *reversed(pos), steps)
    steps = _find_fastest_way(valley, max_x, max_y, *pos, steps)

    return steps


assert find_fastest_way_p2(*ex2) == 54

ANSWER = find_fastest_way_p2(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 896  # check with accepted answer
