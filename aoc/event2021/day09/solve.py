from functools import reduce
from operator import mul

########
# PART 1

def read(filename):
    with open("event2021/day09/" + filename, "r") as file:
        return [[int(ch) for ch in line.strip()] for line in file]


def is_low_point(heightmap, cur_height, x, y):
    width, height = len(heightmap[0]), len(heightmap)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (0 <= x + dx < width) and (0 <= y + dy < height):
            if heightmap[y+ dy][x + dx] <= cur_height:
                return False
    
    return True


def find_low_points(heightmap):
    low_points = []

    for y, row in enumerate(heightmap):
        for x, height in enumerate(row):
            if is_low_point(heightmap, height, x, y):
                low_points += [(x, y, height)]

    return low_points


def risk_level(low_points):
    return sum([height + 1 for _, _, height in low_points])


ex1 = read("example1.txt")
ex1_low_points = find_low_points(ex1)
assert risk_level(ex1_low_points) == 15

inp = read("input.txt")
low_points = find_low_points(inp)
answer = risk_level(low_points)
print("Part 1 =", answer)
assert answer == 417 # check with accepted answer


########
# PART 2

def get_basin_size(heightmap, low_point):
    width, height = len(heightmap[0]), len(heightmap)
    todo = [low_point]
    done = set()

    basin_size = 0
    while todo:
        (x, y, h) = todo.pop(0)

        if ((x, y) not in done):
            done.add((x, y))
            basin_size += 1

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < width) and (0 <= ny < height):
                    nh = heightmap[ny][nx]
                    if nh < 9:
                        if (nx, ny) not in done:
                            todo.append((nx, ny, nh))

    return basin_size


assert reduce(mul, sorted([get_basin_size(ex1, low_point) for low_point in ex1_low_points], reverse = True)[0:3]) == 1134

answer = reduce(mul, sorted([get_basin_size(inp, low_point) for low_point in low_points], reverse = True)[0:3])
print("Part 2 =", answer)
assert answer == 1148965 # check with accepted answer
