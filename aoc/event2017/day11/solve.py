# great article on hexagonal grids:
# https://www.redblobgames.com/grids/hexagons/
# decided for cube coordinates (cause I had this implemented for 2020 and it was easier :D)

import re

########
# PART 1

HEX_DIRECTIONS = {
            'n' : ( 0, -1, +1),
            'ne': (+1, -1,  0),
            'se': (+1,  0, -1),
            's' : ( 0, +1, -1),
            'nw': (-1,  0, +1),
            'sw': (-1, +1,  0)}


def read(filename):
    with open("event2017/day11/" + filename, "r") as file:
        return file.readline().strip()


def distance(p):
    return max(map(abs, p))


def parse(directions):
    pattern = re.compile(r"(e|se|sw|w|nw|ne)")

    instructions = pattern.findall(directions)

    pos = (0, 0, 0)
    max_distance = 0
    for instruction in instructions:
        pos = tuple(sum(x) for x in zip(pos, HEX_DIRECTIONS[instruction]))
        max_distance = max(max_distance, distance(pos))

    return pos, max_distance


# ne,ne,ne is 3 steps away.
assert distance(parse("ne,ne,ne")[0]) == 3
# ne,ne,sw,sw is 0 steps away (back where you started).
assert distance(parse("ne,ne,sw,sw")[0]) == 0
# ne,ne,s,s is 2 steps away (se,se).
assert distance(parse("ne,ne,s,s")[0]) == 2
# se,sw,se,sw,sw is 3 steps away (s,s,sw).
assert distance(parse("se,sw,se,sw,sw")[0]) == 3


inp = read("input.txt")
pos, max_distance = parse(inp)
answer = distance(pos)
print("Part 1 =", answer)
assert answer == 761 # check with accepted answer


########
# PART 2


# ne,ne,ne is 3 steps away.
assert parse("ne,ne,ne")[1] == 3
# ne,ne,sw,sw is 0 steps away (back where you started).
assert parse("ne,ne,sw,sw")[1] == 2
# ne,ne,s,s is 2 steps away (se,se).
assert parse("ne,ne,s,s")[1] == 2
# se,sw,se,sw,sw is 3 steps away (s,s,sw).
assert parse("se,sw,se,sw,sw")[1] == 3

# was retrofitted into the calculation for part 1
answer = max_distance
print("Part 2 =", answer)
assert answer == 1542 # check with accepted answer
