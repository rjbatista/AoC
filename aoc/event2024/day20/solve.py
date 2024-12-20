""" Advent of code 2024 - day 20 """

import heapq
from itertools import combinations
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
        w, h = 0, 0
        for y, line in enumerate(file):
            h = y
            for x, ch in enumerate(line):
                w = x
                if ch == '#':
                    maze.add((x, y))
                elif ch == 'S':
                    start = x, y
                elif ch == 'E':
                    end = x, y

        return maze, start, end, (w, h)


def find_path(maze: set[Coord], start: Coord, end: Coord, size: Coord):
    """ find the shortest paths """
    def trace_path(visited: dict[Coord, tuple[int, Coord]], pos: Coord) -> list[Coord]:
        path = []
        while True:
            score, new_pos = visited[pos]

            path.append((score, pos))

            if new_pos == pos:
                break

            pos = new_pos

        return path

    visited = {}
    todo = []
    width, height = size

    heapq.heappush(todo, (0, start, start))
    while todo:
        score, pos, origin = heapq.heappop(todo)

        if pos in visited:
            continue

        if score < visited.get(pos, (inf, None))[0]:
            visited[pos] = score, origin

        if pos == end:
            return score, trace_path(visited, end)

        x, y = pos
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if (0 <= nx <= width and 0 <= ny <= height
                and (nx, ny) not in maze
                    and (nx, ny) not in visited):

                heapq.heappush(todo, (score + 1, (nx, ny), (x, y)))

    return None


def find_shortcuts(path: list[Coord], cheat_size: int = 2, min_save: int = 1):
    """ find shortcuts in path """
    cheats = 0

    for (s1, p1), (s2, p2) in combinations(path, 2):
        dist = sum(abs(a - b) for a, b in zip(p1, p2))
        if dist <= cheat_size and abs(s2 - s1) - dist >= min_save:
            cheats += 1

    return cheats


ex1 = read("example1.txt")
ex1_best, ex1_path = find_path(*ex1)
assert ex1_best == 84
assert find_shortcuts(ex1_path) == 44

inp = read("input.txt")
inp_best, inp_path = find_path(*inp)
ANSWER = find_shortcuts(inp_path, min_save=100)
print("Part 1 =", ANSWER)
assert ANSWER == 1307  # check with accepted answer

########
# PART 2

assert find_shortcuts(ex1_path, 20, 50) == 285

ANSWER = find_shortcuts(inp_path, 20, 100)
print("Part 2 =", ANSWER)
assert ANSWER == 986545  # check with accepted answer
