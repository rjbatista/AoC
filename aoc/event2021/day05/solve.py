import re

########
# PART 1

def read(filename):
    with open("event2021/day05/" + filename, "r") as file:
        pattern = re.compile(r"^(\d+),(\d+) -> (\d+),(\d+)$")
        
        lines = []
        for line in file:
            m = pattern.match(line)
            if m:
                lines += ((int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))),
            else:
                raise RuntimeError("invalid input " + line)

    return lines


def draw_ocean(ocean, max_x, max_y):
    for y in range(0, max_y):
        for x in range(0, max_x):
            print(ocean.get((x, y), '.'), end="")
        print()


def map_lines(lines, diagonals = False, draw = False):
    ocean = {}
    for (x1, y1), (x2, y2) in lines:
        if diagonals or x1 == x2 or y1 == y2: # only horizontal or vertical lines
            dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
            dy = 1 if y2 > y1 else -1 if y2 < y1 else 0
            
            x, y = x1, y1
            while (x != x2 or y != y2):
                ocean[x, y] = ocean.get((x, y), 0) + 1
                x += dx
                y += dy

            ocean[x, y] = ocean.get((x, y), 0) + 1 # inclusive

    if draw:
        draw_ocean(ocean, 10, 10)

    return ocean


ex1 = read("example1.txt")
assert sum([1 for _, v in map_lines(ex1).items() if v > 1]) == 5

inp = read("input.txt")
answer = sum([1 for _, v in map_lines(inp).items() if v > 1])
print("Part 1 =", answer)
assert answer == 7297 # check with accepted answer


########
# PART 2

assert sum([1 for _, v in map_lines(ex1, diagonals=True).items() if v > 1]) == 12

answer = sum([1 for _, v in map_lines(inp, diagonals=True).items() if v > 1])
print("Part 2 =", answer)
assert answer == 21038 # check with accepted answer
