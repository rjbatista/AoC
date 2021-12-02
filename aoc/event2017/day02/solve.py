import re
from itertools import combinations

########
# PART 1

def read(filename):
    """ parse the input """

    with open("event2017/day02/" + filename, "r") as file:
        return [list(map(int, re.split(r"\s", row.strip()))) for row in file.readlines()]


def calc_checksum(sheet):
    return sum([max(x) - min(x) for x in sheet])


ex1 = read("example1.txt")
assert calc_checksum(ex1) == 18

inp = read("input.txt")
answer = calc_checksum(inp)
print("Part 1 =", answer)
#assert answer == 1044 # check with accepted answer


########
# PART 2

def calc_evenly_divisible(sheet):
    return sum([int(max(a, b) / min(a, b)) for x in sheet for (a, b) in combinations(x, 2) if max(a, b) % min(a, b) == 0])


ex2 = read("example2.txt")
assert calc_evenly_divisible(ex2) == 9

answer = calc_evenly_divisible(inp)
print("Part 2 =", answer)
assert answer == 312 # check with accepted answer
