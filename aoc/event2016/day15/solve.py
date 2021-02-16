import re

########
# PART 1

_debug = False

"""
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

def read_input():
    with open("event2016/day15/input.txt") as f:
        ret = []
        for line in f:
            ret += [line]

    return ret


def read_disc(s):
    m = re.match(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', s)

    return [int(m.group(1)), int(m.group(2)), int(m.group(3))]


def read_discs(disc_list):
    discs = {}
    for s in disc_list:
        id, positions, starting = read_disc(s)

        discs[id] = (starting, positions)

    return discs


def tick(discs):
    for key, (position, positions) in discs.items():
        discs[key] = ((position + 1) % positions, positions)


def p1_solve_for(discs):
    capsules = {}
    t = 0
    res = None
    while not res:
        # add new one
        capsules[t] = 0

        t += 1

        capsules = {k: v + 1 for k, v in capsules.items() if v == 0 or discs[v][0] == 0}
        tick(discs)

        if _debug: print(t, discs, capsules)

        for k, v in capsules.items():
            if v == len(discs) + 1:
                res = k

    return res


example_text = [
    "Disc #1 has 5 positions; at time=0, it is at position 4.",
    "Disc #2 has 2 positions; at time=0, it is at position 1."
]

#example = read_discs(example_text)
#print("won starting at t =", p1_solve_for(example))

p1 = read_discs(read_input())
answer = p1_solve_for(p1)
print("Part 1 =", answer)
assert answer == 203660 # check with accepted answer

########
# PART 2

p2 = read_discs(read_input())
p2[len(p2) + 1] = (0, 11)

answer = p1_solve_for(p2)
print("Part 2 =", answer)
assert answer == 2408135 # check with accepted answer

"""
When it's done, the discs are back in their original configuration as if it were time=0 again,
but a new disc with 11 positions and starting at position 0 has appeared exactly one second below the previously-bottom disc.
"""
