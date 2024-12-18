""" Advent of code 2024 - day 18 """

import heapq
from itertools import count
from math import inf
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def read(filename: str) -> tuple[set[Coord], Coord, Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        maze = {}
        for ns, line in enumerate(file):
            x, y = map(int, line.strip().split(','))
            maze[x, y] = ns

        return maze


def find_path(maze_log: dict[Coord, int], start: Coord, end: Coord, time: int):
    """ find the shortest paths """

    visited = {}
    todo = []
    width, height = end

    heapq.heappush(todo, (0, start))
    while todo:
        score, pos = heapq.heappop(todo)

        if pos in visited:
            continue

        if pos == end:
            return score

        visited[pos] = score

        x, y = pos
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if (0 <= nx <= width and 0 <= ny <= height
                and maze_log.get((nx, ny), inf) >= time
                    and (nx, ny) not in visited):

                heapq.heappush(todo, (score + 1, (nx, ny)))

    return None


ex1 = read("example1.txt")
assert find_path(ex1, (0, 0), (6, 6), 12) == 22

inp = read("input.txt")
ANSWER = find_path(inp, (0, 0), (70, 70), 1024)
print("Part 1 =", ANSWER)
assert ANSWER == 314  # check with accepted answer

########
# PART 2


def find_a_path(maze_log: dict[Coord, int], start: Coord, end: Coord, time: int) -> bool:
    """ find if a path exists, not the shortest """

    visited = set()
    todo = []
    width, height = end

    heapq.heappush(todo, (0, start))
    while todo:
        _, pos = heapq.heappop(todo)

        if pos in visited:
            continue

        if pos == end:
            return True

        visited.add(pos)

        x, y = pos
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if (0 <= nx <= width and 0 <= ny <= height
                and maze_log.get((nx, ny), inf) >= time
                    and (nx, ny) not in visited):

                # use Manhattan distance as heuristic
                heapq.heappush(todo, (height - ny + width - nx, (nx, ny)))

    return False


def find_maze_cutoff(maze_log: dict[Coord, int], start: Coord, end: Coord, known_good: int):
    """ Find out when the maze cuts off """
    for i in count(known_good):
        if not find_a_path(maze_log, start, end, i):
            return [pos for pos, v in maze_log.items() if v == i - 1][0]

    return None


assert find_maze_cutoff(ex1, (0, 0), (6, 6), 12) == (6, 1)

ANSWER = find_maze_cutoff(inp, (0, 0), (70, 70), 1024)
print("Part 2 =", ANSWER)
assert ANSWER == (15, 20)  # check with accepted answer
