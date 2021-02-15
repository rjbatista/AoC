import re

########
# PART 1

def get_rules(fn):
    can_be_inside_of = {}
    bags_contained = {}
    with open("event2020/day07/" + fn, "r") as input:
        linePattern = re.compile(r"^(\w+ \w+) bags contain (no other bags|(?: ?\d+ \w+ \w+ bags?,?)+)\.$")
        insidePattern = re.compile(r" ?(\d+) (\w+ \w+) bags?,?")

        for line in input:
            m = linePattern.match(line)
            if m:
                if m.group(2) != 'no other bags':
                    for count, bag in insidePattern.findall(m.group(2)):
                        bags_contained[m.group(1)] = bags_contained.get(m.group(1), []) + [(int(count), bag)]
                        can_be_inside_of[bag] = can_be_inside_of.get(bag, []) + [m.group(1)]
            else:
                raise RuntimeError
            pass
    return can_be_inside_of, bags_contained


def possible_bags(can_be_inside_of, bag):
    if bag not in can_be_inside_of:
        return None

    all_possible = set()
    for possibility in can_be_inside_of[bag]:
        all_possible.add(possibility)

        other = possible_bags(can_be_inside_of, possibility)
        if (other):
            all_possible = all_possible.union(other)

    return all_possible


assert len(possible_bags(get_rules("example1.txt")[0], "shiny gold")) == 4

rules = get_rules("input.txt")
answer = len(possible_bags(rules[0], "shiny gold"))
print("Part 1 =", answer)
assert answer == 161 # check with accepted answer

########
# PART 2

def count_all(bags_contained, bag):
    total_count = 1
    if (bag in bags_contained):
        for count, inside_bag in bags_contained[bag]:
            total_count += count * count_all(bags_contained, inside_bag)

    return total_count

assert count_all(get_rules("example1.txt")[1], "shiny gold") - 1 == 32
assert count_all(get_rules("example2.txt")[1], "shiny gold") - 1 == 126

answer = count_all(rules[1], "shiny gold") - 1
print("Part 2 =", answer)
assert answer == 30899 # check with accepted answer
