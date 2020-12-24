# great article on hexagonal grids:
# https://www.redblobgames.com/grids/hexagons/
# decided for cube coordinates

import re

########
# PART 1
HEX_DIRECTIONS = {
            'e' : (+1, -1,  0),
            'se': ( 0, -1, +1),
            'sw': (-1,  0, +1),
            'w' : (-1, +1,  0),
            'nw': ( 0, +1, -1),
            'ne': (+1,  0, -1)}

def read_grid(fn):
    with open("event2020/day24/" + fn, "r") as file:
        pattern = re.compile(r"e|se|sw|w|nw|ne")
        
        grid = {}
        for line in file:
            instructions = pattern.findall(line)

            pos = (0, 0, 0)
            for instruction in instructions:
                pos = tuple(sum(x) for x in zip(pos, HEX_DIRECTIONS[instruction]))

            grid[pos] = not (grid.get(pos, False))
    
    return grid


def count_blacks(grid):
    return sum([1 for (x, y, z), blk in grid.items() if blk])


assert count_blacks(read_grid("example1.txt")) == 10

grid = read_grid("input.txt")
answer = count_blacks(grid)
print("Part 1 =", answer)
assert answer == 354 # check with accepted answer

########
# PART 2

def flip_neighbours(grid):
    to_flip = []
    to_check = list(grid.items())
    accounted = set(grid.keys())
    while to_check:
        pos, blk = to_check.pop()

        count = 0
        for direction in HEX_DIRECTIONS.values():
            neighbour_pos = pos[0] + direction[0], pos[1] + direction[1], pos[2] + direction[2]

            if blk and neighbour_pos not in accounted:
                to_check.append((neighbour_pos, grid.get(neighbour_pos, False)))
                accounted.add(neighbour_pos)

            count += 1 if grid.get(neighbour_pos, False) else 0
        
        if blk:
            # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
            if count == 0 or count > 2:
                to_flip += [pos]
        else:
            # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
            if count == 2:
                to_flip += [pos]

    for pos in to_flip:
        grid[pos] = not grid.get(pos, False)


def print_grid(grid):
    def oddr_to_cube(row, col):
        x = col - (row - (row & 1)) / 2
        z = row
        y = -x-z
        return x, y, z

    for row in range(-4, 4):
        if row % 2 == 0:
            print(end = " ")

        for col in range(-4, 4):
            x, y, z = oddr_to_cube(row, col)

            print('#' if grid.get((x, y, z), False) else '.', end = " ")
        print()


# check example
grid = read_grid("example1.txt")
# Day 1: 15
flip_neighbours(grid)
assert count_blacks(grid) == 15
# Day 2: 12
flip_neighbours(grid)
assert count_blacks(grid) == 12
# Day 3: 25
flip_neighbours(grid)
assert count_blacks(grid) == 25
# Day 4: 14
flip_neighbours(grid)
assert count_blacks(grid) == 14
# Day 5: 23
flip_neighbours(grid)
assert count_blacks(grid) == 23
# Day 6: 28
flip_neighbours(grid)
assert count_blacks(grid) == 28
# Day 7: 41
flip_neighbours(grid)
assert count_blacks(grid) == 41
# Day 8: 37
flip_neighbours(grid)
assert count_blacks(grid) == 37
# Day 9: 49
flip_neighbours(grid)
assert count_blacks(grid) == 49
# Day 10: 37
flip_neighbours(grid)
assert count_blacks(grid) == 37
# Day 100: 2208
for _ in range(90):
    flip_neighbours(grid)
assert count_blacks(grid) == 2208

# check with input
grid = read_grid("input.txt")
for _ in range(100):
    flip_neighbours(grid)
answer = count_blacks(grid)
print("Part 2 =", answer)
assert answer == 3608 # check with accepted answer
