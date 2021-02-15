import re

########
# PART 1

def process_line(line):
    m = re.match(r"Sue (\d+): (.*)", line)
    sue = int(m.group(1))

    props = {}
    for (x, y) in re.findall(r"(\w*): (\d*)(?:, )?", m.group(2)):
        props[x] = int(y)

    return sue, props


def process_file(fn):
    with open(fn) as f:
        ret = {}
        for line in f:
            name, prop = process_line(line)
            ret[name] = prop

        return ret


def match_value(key, have, wanted):
    if (key in ['cats', 'trees']):
        return have > wanted
    elif (key in ['pomeranians', 'goldfish']):
        return have < wanted
    else:
        return have == wanted


def match(wanted, have):
    return sum([1 for h in have if wanted[h] == have[h]]) == len(have)


def search(wanted, known, match_function = match):
    for sue, props in known.items():
        if (match_function(wanted, props)):
            return sue


_, wanted = process_line("Sue 0: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1")
known = process_file("event2015/day16/input.txt")

answer = search(wanted, known)
print("Part 1 =", answer)
assert answer == 373 # check with accepted answer

########
# PART 2

def match_p2(wanted, have):
    return sum([1 for h in have if match_value(h, have[h], wanted[h])]) == len(have)


answer = search(wanted, known, match_p2)
print("Part 2 =", answer)
assert answer == 260 # check with accepted answer
