import re

########
# PART 1

directions = ['N', 'E', 'S', 'W']

def read_input():
    with open("event2016/day01/input.txt") as f:
        return [(x[0], int(x[1:])) for x in re.split(r'\s*,\s*', f.read())]


def forward(player, units):
    dir = player[2]

    if (directions[dir] == 'N'):
        player[1] -= units
    elif (directions[dir] == 'E'):
        player[0] += units
    elif (directions[dir] == 'S'):
        player[1] += units
    elif (directions[dir] == 'W'):
        player[0] -= units


def p1_solve_for(input, player):
    #print(input)
    #print("starting =", player)

    for move in input:
        if (move[0] == 'L'):
            player[2] = (player[2] + 1) % len(directions)
        elif (move[0] == 'R'):
            player[2] = (player[2] + 3) % len(directions)

        forward(player, move[1])

    dist = abs(player[0]) + abs(player[1])
    #print("ending =", player, "distance", dist)

    return dist

assert p1_solve_for([ ('R', 2), ('L', 3) ], [0, 0, 0]) == 5
assert p1_solve_for([ ('R', 2), ('R', 2), ('R', 2) ], [0, 0, 0]) == 2
assert p1_solve_for([ ('R', 5), ('L', 5), ('R', 5), ('R', 3) ], [0, 0, 0]) == 12

answer = p1_solve_for(read_input(), [0, 0, 0])
print("Part 1 =", answer)
assert answer == 209 # check with accepted answer


########
# PART 2

def p2_solve_for(input, player):
    #print(input)
    #print("starting =", player)
    visited = []
    is_visited = False

    for move in input:
        if (move[0] == 'L'):
            player[2] = (player[2] + 1) % len(directions)
        elif (move[0] == 'R'):
            player[2] = (player[2] + 3) % len(directions)

        for _ in range(move[1]):
            forward(player, 1)

            pos = (player[0], player[1])
            if (pos in visited):
                is_visited = True
                break

            visited += [pos]

        if (is_visited): break

    dist = abs(player[0]) + abs(player[1])
    #print("ending =", player, "distance", dist)

    return dist


assert p2_solve_for([ ('R', 8), ('R', 4), ('R', 4), ('R', 8) ], [0, 0, 0]) == 4

answer = p2_solve_for(read_input(), [0, 0, 0])
print("Part 2 =", answer)
assert answer == 136 # check with accepted answer
