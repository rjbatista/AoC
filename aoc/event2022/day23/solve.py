""" Advent of code 2022 - day 23 """
from pathlib import Path
from math import inf
from collections import deque

########
# PART 1

DIRECTIONS = deque([(0, -1), (0, 1), (-1, 0), (1, 0)])


def decide(pos: tuple[int, int], grove: set) -> tuple[int, int]:
    x, y = pos
    should_move = False
    decided = None

    for dx, dy in DIRECTIONS:
        count = 0
        for diff in range(-1, 2):
            test_x = dx if dx != 0 else diff
            test_y = dy if dy != 0 else diff

            pos_x, pos_y = x + test_x, y + test_y

            count += 1 if (pos_x, pos_y) in grove else 0

        if count > 0:
            should_move = True

        if count == 0 and decided is None:
            decided = (x + dx, y + dy)

    # don't move
    return decided if should_move else None


def read(filename: str) -> set:
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        grove = set()
        for y, line in enumerate(file):
            for x, char in enumerate(line):
                if char == '#':
                    grove.add((x, y))

        return grove


def do_round(grove: set):
    new_grove = {}

    # decide
    count_unmoved = 0
    for pos in grove:
        decision = decide(pos, grove)

        if decision is None:
            count_unmoved += 1
            decision = pos

        new_grove.setdefault(decision, []).append(pos)

    DIRECTIONS.rotate(-1)

    if count_unmoved == len(grove):
        return False

    # commit
    for (x, y), elves in new_grove.items():
        if len(elves) == 1:
            grove.remove(elves[0])
            grove.add((x, y))

    return True


def draw_grove(grove: set):
    min_x = min_y = -1
    max_x = max_y = 5
    for (x, y) in grove.keys():
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

    print(' ', ' ' * min_x, '0', (min_x, max_x))
    for y in range(min_y, max_y + 1):
        print('0 ' if y == 0 else '  ',  end="")
        for x in range(min_x, max_x + 1):
            print('#' if (x, y) in grove else '.', end="")
        print()
    print()


def count_ground(grove: set):
    min_x = min_y = inf
    max_x = max_y = -inf
    for (x, y) in grove:
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(grove)


# ex1 = read("example1.txt")
# draw_grove(ex1)

ex2 = read("example2.txt")
for i in range(1, 11):
    do_round(ex2)
assert count_ground(ex2) == 110


inp = read("input.txt")
for _ in range(10):
    do_round(inp)
ANSWER = count_ground(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 4249  # check with accepted answer

########
# PART 2


def do_until_all_stop(grove):
    count = 1
    while do_round(grove):
        count += 1

    return count


assert do_until_all_stop(read("example2.txt")) == 20

ANSWER = do_until_all_stop(read("input.txt"))
print("Part 2 =", ANSWER)
assert ANSWER == 980  # check with accepted answer
