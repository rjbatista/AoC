import re

########
# PART 1

def parse_p1(line):
    return eval("str(" + line + ")")


########
# PART 2

def parse_p2(line):
    parsed_p2 = re.sub(r"\\", r"\\\\", line)
    parsed_p2 = re.sub(r"\"", r"\"", parsed_p2)
    parsed_p2 = re.sub(r"\\(x[0-9,a-f,A-F]{2})", r"\\\1", parsed_p2)

    parsed_p2 = "\"" + parsed_p2 + "\""

    return parsed_p2


def run():
    diff = 0
    diff_p2 = 0

    with open('event2015/day08/input.txt', 'r') as f:
        for line in f:
            if line[-1] == '\n': line = line[:-1]

            parsed = parse_p1(line)
            parsed_p2 = parse_p2(line)

            diff += len(line) - len(parsed)
            diff_p2 += len(parsed_p2) - len(line)

    return diff, diff_p2


p1, p2 = run()

print("Part 1 =", p1)
assert p1 == 1333 # check with accepted answer

print("Part 2 =", p2)
assert p2 == 2046 # check with accepted answer
