""" Advent of code 2017 - day 10 """
from pathlib import Path
from functools import reduce
from operator import mul
from event2017.day10.knot_hash import knot_hash_round, knot_hash

########
# PART 1

def read(filename):
    """ Read the input """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        return list(map(int, file.readline().strip().split(',')))


assert reduce(mul, knot_hash_round([3, 4, 1, 5], 5)[0:2]) == 12


inp = read("input.txt")
answer = reduce(mul, knot_hash_round(inp)[0:2])
print("Part 1 =", answer)
assert answer == 11413 # check with accepted answer


########
# PART 2

def read_as_ascii(filename):
    """ Read the input as ascii """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        return file.readline().strip()


def dense_hash(sparse_hash):
    """ Perform the dense hash """
    hash = [0] * 16

    for idx, v in enumerate(sparse_hash):
        hash[int(idx / 16)] ^= v

    return ''.join(["%02x" % x for x in hash])


def knot_hash(input_str : str):
    """ Return the know hash of the input  """
    inp_list = list(map(ord, input_str)) + [ 17, 31, 73, 47, 23 ]

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
