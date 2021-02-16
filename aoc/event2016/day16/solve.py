########
# PART 1

def dragon_step(a):
    """
    For example, after a single step of this process,

    1 becomes 100.
    0 becomes 001.
    11111 becomes 11111000000.
    111100001010 becomes 1111000010100101011110000
    """

    b = [0 if x==1 else 1 for x in a]
    b.reverse()

    return a + [0] + b


def checksum(input):
    """
    Consider each pair: 11, 00, 10, 11, 01, 00.
    These are same, same, different, same, different, same, producing 110101.
    The resulting string has length 6, which is even, so we repeat the process.
    The pairs are 11 (same), 01 (different), 01 (different).
    This produces the checksum 100, which has an odd length, so we stop.
    """

    calc = [1 if a == b else 0 for a, b in zip(input[::2], input[1::2])]
    if len(calc) % 2 == 0:
        calc = checksum(calc)

    return calc


def generate_disc(disc, length):
    while len(disc) < length:
        disc = dragon_step(disc)

    return disc[:length]


assert dragon_step([1]) == [1, 0, 0]
assert dragon_step([0]) == [0, 0, 1]
assert dragon_step([1,1,1,1,1]) == [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
assert dragon_step([1,1,1,1,0,0,0,0,1,0,1,0]) == [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0]
assert checksum([1,1,0,0,1,0,1,1,0,1,0,0]) == [1, 0, 0]

example = generate_disc([1,0,0,0,0], 20)
assert checksum(example) == [0,1,1,0,0]

p1 = generate_disc([1,0,0,1,1,1,1,1,0,1,1,0,1,1,0,0,1], 272)

answer = "".join(map(str, checksum(p1)))
print("Part 1 =", answer)
assert answer == "10111110010110110" # check with accepted answer

########
# PART 2

p2 = generate_disc([1,0,0,1,1,1,1,1,0,1,1,0,1,1,0,0,1], 35651584)

answer = "".join(map(str, checksum(p2)))
print("Part 2 =", answer)
assert answer == "01101100001100100" # check with accepted answer
