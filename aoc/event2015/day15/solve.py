import re
import itertools
from functools import reduce

########
# PART 1

def process_line(line):
    '''
    return name, (capacity, durability, flavor, texture, calories)
    '''
    m = re.match(r"(.+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)", line)

    return m.group(1), (int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))


def process_file(fn):
    with open(fn) as f:
        ret = {}
        for line in f:
            name, prop = process_line(line)
            ret[name] = prop

        return ret


def value_of(ing, rec):
    props = [tuple(v * e for e in ing[i]) for (v, i) in rec]
    props = [max(0, sum(e)) for e in zip(*props)]

    return reduce(lambda x,y: x*y, props[:-1])


def value_of_with_cal(ing, rec):
    props = [tuple(v * e for e in ing[i]) for (v, i) in rec]
    props = [max(0, sum(e)) for e in zip(*props)]

    if (props[-1] != 500): return 0

    return reduce(lambda x,y: x*y, props[:-1])


def try_all(remaining, subset):
    if (len(subset) == 1):
        return [[tuple((remaining, subset[0]))]]
    elif (len(subset) == remaining):
        return [[tuple((1, each)) for each in subset]]

    combs = []
    for i in range(remaining - (len(subset) - 1), 0, -1):
        others = try_all(remaining - i, subset[1:])
        combs += [[(i, subset[0])] + other for other in others]

    return combs


def combinations(number, element):
    if (element == 1):
        return [[number]]

    combs = []
    for i in range(1, number):
        others = combinations(number - i, element - 1)
        combs += [[i] + other for other in others]

    return combs


def run():
    ing = process_file('event2015/day15/input.txt')

    max_val = 0
    max_val2 = 0

    for L in range(1, len(ing) + 1):
        for subset in itertools.combinations(ing, L):
            recs = try_all(100, list(subset))
            for rec in recs:
                max_val = max(max_val, value_of(ing, rec))
                max_val2 = max(max_val2, value_of_with_cal(ing, rec))
    
    return max_val, max_val2


max_val, max_val2 = run()

answer = max_val
print("Part 1 =", answer)
assert answer == 21367368 # check with accepted answer

########
# PART 2

answer = max_val2
print("Part 2 =", answer)
assert answer == 1766400 # check with accepted answer
