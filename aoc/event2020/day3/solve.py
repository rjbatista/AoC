from functools import reduce
from operator import mul

########
# PART 1
def get_map(fn):
    ret = []
    width = 0
    with open("event2020/day3/" + fn, "r") as input:
        for line in input:
            val = 0
            width = len(line) - 1
            for i, ch in enumerate(line):
                if (ch == '#'):
                    val |= 1 << i
            ret.append(val)
        
    return width, ret

def get_collisions(width, area, slope):
    max_y = len(area)
    x, y = 0, 0
    slope_x, slope_y = slope
    count = 0
    while y < max_y:
        count += 0 if (area[y] & 1 << (x % width)) == 0 else 1
        x, y = x + slope_x, y + slope_y
    
    return count

assert get_collisions(*get_map("example1.txt"), (3, 1)) == 7
answer = get_collisions(*get_map("input.txt"), (3, 1))
print("Part 1 =", answer)
assert answer == 148 # check with accepted answer

########
# PART 2
def get_answer(width, area):
    total = []
    for slope in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
        total.append(get_collisions(width, area, slope))

    return reduce(mul, total)

answer = get_answer(*get_map("input.txt"))
print("Part 2 =", answer)
assert answer == 727923200 # check with accepted answer
