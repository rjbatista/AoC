""" Advent of code 2017 - day 14 """
from pathlib import Path
from event2017.day10.knot_hash import knot_hash


########
# PART 1

def create_grid_from_key(key):
    """ create the grid from the key """
    grid = []
    for i in range(128):
        grid.append(list(bin(int(knot_hash(f"{key}-{i}"), 16))[2:].zfill(128)))

    return grid


ex1 = create_grid_from_key('flqrgnkx')
assert (sum(1 for row in ex1 for bit in row if bit == '1')) == 8108

inp = create_grid_from_key('ugkiagan')
answer = sum(1 for row in inp for bit in row if bit == '1')
print("Part 1 =", answer)
assert answer == 8292 # check with accepted answer

########
# PART 2

def remove_region(grid: list, pos_x: int, pos_y: int):
    """ remove a region from the grid """
    stack = [(pos_x, pos_y)]

    while stack:
        pos_x, pos_y = stack.pop()
        grid[pos_y][pos_x] = '0'

        for d_x, d_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (0 <= pos_x + d_x < len(grid[0])
                and  0 <= pos_y + d_y < len(grid[0])
                and grid[pos_y + d_y][pos_x + d_x] == '1'):

                stack.append((pos_x + d_x, pos_y + d_y))


def search_regions(grid) -> int:
    """ search the grid for regions """

    total_regions = 0
    for pos_y, row in enumerate(grid):
        for pos_x, bit in enumerate(row):
            if bit == '1':
                total_regions += 1
                remove_region(grid, pos_x, pos_y)

    return total_regions


assert search_regions(ex1) == 1242

answer = search_regions(inp)
print("Part 2 =", answer)
assert answer == 1069 # check with accepted answer
