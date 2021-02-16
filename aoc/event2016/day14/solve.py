import re
from hashlib import md5

########
# PART 1

_debug = False

def calc_hash(salt, index, stretch):
    msg = (salt + str(index)).encode('utf-8')

    h = md5(msg).hexdigest()

    if stretch:
        #h = md5(h.encode('utf-8')).hexdigest()
        hh = md5(msg)
        for _ in range(2016):
            h = md5(h)

    return h


def get_block(salt, index, needed, stretch):
    if _debug: print("calculating block from", index, index + needed)

    block = []
    for i in range(needed):
        block.append(calc_hash(salt, index + i, stretch))

    return block, index, index + needed


def has_fives(c, h):
    return re.search(r"%s{5}" % c, h)


def find_keys(salt, stretch = False):
    block = [], 0, 0
    found = 0

    trips_pattern = re.compile(r'(\w)\1\1')

    index = 0
    while found < 64:
        trips = None
        while not trips:
            if index >= block[2]:
                block = get_block(salt, index, 1000, stretch)

            trips = trips_pattern.search(block[0][index - block[1]])

            if not trips:
                index += 1

        trips = trips.group(1), index

        if _debug: print("trips", trips[0], "at", trips[1])

        # get remaining block for fives
        if index + 1000 >= block[2]:
            rblock = get_block(salt, block[2], index - block[1] + 1001 - block[2], stretch)
            block = block[0] + rblock[0], block[1], rblock[2]

        found_five = False

        if _debug: print("searching from %d to %d in %d-%d" % (index + 1, index + 1001, block[1], block[2]))

        fives_pattern = re.compile("[%s]{5}" % trips[0])
        for findex in range(index + 1, index + 1001):
            if fives_pattern.search(block[0][findex - block[1]]):
                found_five = True
                break

        if found_five:
            if _debug: print("found fives at", findex)
            found += 1

        index += 1

    return index - 1


#keys = find_keys("abc")

answer = find_keys("qzyelonm")
print("Part 1 =", answer)
assert answer == 15168 # check with accepted answer

########
# PART 2

answer = find_keys("qzyelonm", True)
print("Part 2 =", answer)
assert answer == 20864 # check with accepted answer
