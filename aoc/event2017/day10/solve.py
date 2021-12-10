from functools import reduce
from operator import mul

########
# PART 1

def read(filename):
    with open("event2017/day10/" + filename, "r") as file:
        return list(map(int, file.readline().strip().split(',')))


def knot_hash_round(lengths : list, list_size = 256, rounds = 1):
    inp = list(range(list_size))

    pos = 0
    skip = 0

    for _ in range(rounds):
        for length in lengths:

            end_pos = pos + length
            if end_pos > list_size:
                selected = inp[pos:] + inp[:end_pos % list_size]
            else:
                selected = inp[pos:end_pos]

            for p in range(length):
                inp[(pos + p) % list_size] = selected[length - p - 1]

            pos = (pos + length + skip) % list_size
            skip += 1

    return inp


assert reduce(mul, knot_hash_round([3, 4, 1, 5], 5)[0:2]) == 12


lengths = read("input.txt")
answer = reduce(mul, knot_hash_round(lengths)[0:2])
print("Part 1 =", answer)
assert answer == 11413 # check with accepted answer


########
# PART 2

def read_as_ascii(filename):
    with open("event2017/day10/" + filename, "r") as file:
        return file.readline().strip()


def dense_hash(sparse_hash):
    hash = [0] * 16

    for idx, v in enumerate(sparse_hash):
        hash[int(idx / 16)] ^= v

    return ''.join(["%02x" % x for x in hash])


def knot_hash(inp : str):
    inp_list = list(map(ord, inp)) + [ 17, 31, 73, 47, 23 ]

    return dense_hash(knot_hash_round(inp_list, rounds = 64))


# The empty string becomes a2582a3a0e66e6e86e3812dcb672a272.
assert knot_hash("") == "a2582a3a0e66e6e86e3812dcb672a272"
# AoC 2017 becomes 33efeb34ea91902bb2f59c9920caa6cd.
assert knot_hash("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
# 1,2,3 becomes 3efbe78a8d82f29979031a4aa0b16a9d.
assert knot_hash("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
# 1,2,4 becomes 63960835bcdc130f0b66d7ff4f6a5a8e.
assert knot_hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"


inp_p2 = read_as_ascii("input.txt")
answer = knot_hash(inp_p2)
print("Part 2 =", answer)
assert answer == "7adfd64c2a03a4968cf708d1b7fd418d" # check with accepted answer
