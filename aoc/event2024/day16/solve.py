""" Advent of code 2024 - day 16 """

import heapq
from math import inf
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def read(filename: str) -> tuple[set[Coord], Coord, Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        start, end = None, None
        maze = set()
        for y, line in enumerate(file):
            for x, ch in enumerate(line):
                if ch == '#':
                    maze.add((x, y))
                elif ch == 'S':
                    start = x, y
                elif ch == 'E':
                    end = x, y

        return maze, start, end


def find_path(maze: set[Coord], start: Coord, end: Coord):
    """ find all shortest paths (solves part 2 instead of stoping at best ) """

    visited = {}
    todo = []
    best = inf
    best_paths = []

    heapq.heappush(todo, (0, start, 0, [start]))
    while todo:
        score, pos, dir_idx, path = heapq.heappop(todo)

        if score > best:
            # all solutions after this are worst, so just end
            break

        if (pos, dir_idx) in visited and visited[(pos, dir_idx)] < score:
            # not worth it, skip
            continue

        visited[(pos, dir_idx)] = score
        if pos == end:
            best = score
            best_paths.append(path)

        x, y = pos
        for i in range(-1, 2):
            new_dir = (dir_idx + i) % len(DIRECTIONS)
            dx, dy = DIRECTIONS[new_dir]

            nx, ny = x + dx, y + dy

            if (nx, ny) not in maze:
                heapq.heappush(todo, (score + (1 if new_dir == dir_idx else 1001),
                                      (nx, ny), new_dir, path + [(nx, ny)]))

    return best, best_paths


ex1 = read("example1.txt")
res_ex1 = find_path(*ex1)
assert res_ex1[0] == 7036

ex2 = read("example2.txt")
res_ex2 = find_path(*ex2)
assert res_ex2[0] == 11048

inp = read("input.txt")
res_inp = find_path(*inp)
ANSWER = res_inp[0]
print("Part 1 =", ANSWER)
assert ANSWER == 102504  # check with accepted answer

########
# PART 2

assert len(set((x, y) for path in res_ex1[1] for x, y in path)) == 45

assert len(set((x, y) for path in res_ex2[1] for x, y in path)) == 64

ANSWER = len(set((x, y) for path in res_inp[1] for x, y in path))
print("Part 2 =", ANSWER)
assert ANSWER == 535  # check with accepted answer
