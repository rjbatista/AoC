""" Advent of code 2022 - day 12 """
from pathlib import Path
from typing import List, Tuple
import heapq
from math import inf

########
# PART 1

def read(filename) -> Tuple[List[int], Tuple[int, int], Tuple[int, int]]:
    """ read heightmap """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        start = end = None
        grid = []
        for pos_y, line in enumerate(file):
            row = []
            for pos_x, char in enumerate(line.strip()):
                if char == 'S':
                    start = (pos_x, pos_y)
                    char = 'a'
                elif char == 'E':
                    end = (pos_x, pos_y)
                    char = 'z'

                row.append(ord(char) - ord('a'))
            grid.append(row)

        return grid, start, end


def shortest_path(grid : List[List[int]], start, end, at_most = inf) -> int:
    """ find the shortest path with at_most steps """

    width = len(grid[0])
    height = len(grid)

    todo = [(0, start)]
    heapq.heapify(todo)

    already_visited = set()
    while todo:
        steps, pos = heapq.heappop(todo)
        pos_x, pos_y = pos

        if pos == end:
            return steps

        if steps + 1 == at_most:
            continue

        for d_x, d_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos_x = pos_x + d_x
            new_pos_y = pos_y + d_y

            if (0 <= new_pos_x < width
                and 0 <= new_pos_y < height
                and grid[new_pos_y][new_pos_x] <= grid[pos_y][pos_x] + 1):

                if (new_pos_x, new_pos_y) not in already_visited:
                    already_visited.add((new_pos_x, new_pos_y))

                    heapq.heappush(todo, (steps + 1, (new_pos_x, new_pos_y)))

    return inf


ex1 = read("example1.txt")
assert shortest_path(*ex1) == 31

inp = read("input.txt")
ANSWER = shortest_path(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 484 # check with accepted answer

########
# PART 2

def shortest_path_from_lowest(grid, end) -> int:
    """ find shortest path from all lowest points """
    possible_starts = [(pos_x, pos_y) for pos_y, row in enumerate(grid)
        for pos_x, char in enumerate(row) if char == 0]

    current_min = inf
    for start in possible_starts:
        current_min = min(current_min, shortest_path(grid, start, end, current_min))

    return current_min


assert shortest_path_from_lowest(ex1[0], ex1[2]) == 29

ANSWER = shortest_path_from_lowest(inp[0], inp[2])
print("Part 2 =", ANSWER)
assert ANSWER == 478 # check with accepted answer
