import re

########
# PART 1


def read_input():
    with open("event2016/day20/input.txt") as f:
        l = []
        for line in f:
            line = line if line[-1] != '\n' else line[:-1]
            l += [tuple(int(a) for a in line.split('-'))]

    return l


def clean_and_get_lowest(inp):
    sorted_input = sorted(inp, key=lambda x: x[0])

    lowest = 0xffffffff
    i = 0
    while i < len(sorted_input) - 1:
        a1, a2 = sorted_input[i]
        b1, b2 = sorted_input[i + 1]

        if b1 <= a2 + 1:
            sorted_input[i] = (a1, max(a2, b2))
            del sorted_input[i + 1]
        else:
            i += 1

            lowest = min(lowest, a2 + 1)

    return lowest, sorted_input


lowest_ip, clean_input = clean_and_get_lowest(read_input())

answer = lowest_ip
print("Part 1 =", answer)
assert answer == 17348574 # check with accepted answer

########
# PART 2

def inverse_list(inp):
    inverse = []

    for (_, a), (b, _) in zip(inp, inp[1:]):
        inverse += [(a + 1, b - 1)]

    # pad endings
    if inp[0][0] != 0:
        inverse = [(0, inp[0][0] - 1)] + inverse

    if inp[-1][1] != 0xffffffff:
        inverse += [(inp[-1][1] + 1, 0xffffffff)]

    return inverse


# valid = inverse_list([(5, 10), (20, 30), (32, 0xffffffff - 1)])
valid = inverse_list(clean_input)

answer = sum([b - a + 1 for a, b in valid])
print("Part 2 =", answer)
assert answer == 104 # check with accepted answer

