import math
import re

########
# PART 1
def get_elements(fn):
    elements = {}
    with open("event2019/day14/" + fn, "r") as file:
        line_pattern = re.compile(r"^((?:\d+ \w+(?:,\s)?)+) => (\d+) (\w+)$")
        element_pattern = re.compile(r"(\d+) (\w+)")
        for line in file:
            m = re.match(line_pattern, line)
            if m:
                elements[m.group(3)] = int(m.group(2)), [(int(c), e) for c, e in re.findall(element_pattern, m.group(1))]

    return elements


def get_ores(elements, required_count, required_element):
    surplus = {}

    def produce(required, element):
        produced, composition = elements[element]

        count = math.ceil(required / produced)
        diff = count * produced - required

        # add extra to surplus
        if diff > 0:
            surplus[element] = surplus.get(element, 0) + diff

        total = 0
        for c, e in composition:
            if e == 'ORE':
                total += c * count
            else:
                # check surplus
                needed = c * count
                if e in surplus:
                    diff = surplus[e] - needed

                    if diff > 0:
                        surplus[e] = diff
                    else:
                        del surplus[e]

                        if (diff < 0):
                            total += produce(-diff, e)
                else:
                    total += produce(needed, e)

        return total

    return produce(required_count, required_element), surplus

assert get_ores(get_elements("example1.txt"), 1, 'FUEL')[0] == 31
assert get_ores(get_elements("example2.txt"), 1, 'FUEL')[0] == 165
assert get_ores(get_elements("example3.txt"), 1, 'FUEL')[0] == 13312
assert get_ores(get_elements("example4.txt"), 1, 'FUEL')[0] == 180697
assert get_ores(get_elements("example5.txt"), 1, 'FUEL')[0] == 2210736

elements = get_elements("input.txt")
answer = get_ores(elements, 1, 'FUEL')
print("Part 1 =", answer[0])
assert answer[0] == 504284 # check with accepted answer

########
# PART 2

# count the extra ores wasted on surplus
def maximize(elements):
    min_ores_for_one, _ = get_ores(elements, 1, 'FUEL')
    count = math.ceil(1000000000000 / min_ores_for_one)

    while True:
        cur_min, _ = get_ores(elements, count, 'FUEL')

        if (cur_min > 1000000000000):
            break

        count += math.ceil((1000000000000 - cur_min) / min_ores_for_one)

    return count - 1

assert maximize(get_elements("example3.txt")) == 82892753
assert maximize(get_elements("example4.txt")) == 5586022
assert maximize(get_elements("example5.txt")) == 460664

answer = maximize(elements)
print("Part 2 =", answer)
assert answer == 2690795 # check with accepted answer
