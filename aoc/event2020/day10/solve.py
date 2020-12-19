########
# PART 1
from functools import reduce

def read_adapters(fn):
    with open("event2020/day10/" + fn, "r") as file:
        adapters = [int(x) for x in file.readlines()]
    
    adapters = (adapters + [max(adapters) + 3]) # add device adapter
    adapters.sort()
    return adapters


def get_differences(adapters):
    return [b - a for a, b in (zip([0] + adapters, adapters))]


def get_answer(differences):
    return sum([1 for x in differences if x == 1]) * sum([1 for x in differences if x == 3])

assert get_answer(get_differences(read_adapters("example1.txt"))) == 7 * 5
assert get_answer(get_differences(read_adapters("example2.txt"))) == 22 * 10

adapters = read_adapters("input.txt")
differences = [b - a for a, b in (zip([0] + adapters, adapters))]
answer = get_answer(differences)
print("Part 1 =", answer)
assert answer == 1700 # check with accepted answer

########
# PART 2

def rle(list):
    rle = []
    count, curr = 1, list[0]
    for element in list[1:]:
        if (element == curr):
            count += 1
        else:
            rle.append((count, curr))
            count, curr = 1, element

    rle.append((count, curr))

    return rle


def arrangements(differences):
    arrangements = { 1: 1, 2: 2, 3: 4, 4: 7}

    return reduce(lambda a, b: a * b, [arrangements[c] for c, e in rle(differences) if e == 1])


assert arrangements(get_differences(read_adapters("example1.txt"))) == 8
assert arrangements(get_differences(read_adapters("example2.txt"))) == 19208

answer = arrangements(differences)
print("Part 2 =", answer)
assert answer == 12401793332096 # check with accepted answer
