import re

########
# PART 1

def calc(expression):
    pattern_group = re.compile(r"^(.*)\((.*?)\)(.*)$")
    pattern_simple = re.compile(r"^(\d+ [+*] \d+)(.*)$")

    while True:
        m = pattern_group.match(expression)
        if m:
            expression = m.group(1) + str(calc(m.group(2))) + m.group(3)
        else:
            break

    while True:
        m = pattern_simple.match(expression)
        if m:
            expression = str(eval(m.group(1))) + m.group(2)
        else:
            break

    return eval(expression)


# 1 + 2 * 3 + 4 * 5 + 6 = 71
assert calc("1 + 2 * 3 + 4 * 5 + 6") == 71

# 2 * 3 + (4 * 5) becomes 26.
assert calc("2 * 3 + (4 * 5)") == 26

# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
assert calc("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437

# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
assert calc("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240

# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
assert calc("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

lines = []
with open("event2020/day18/input.txt", "r") as file:
    for line in file:
        lines.append(calc(line[:-1]))

answer = sum(lines)
print("Part 1 =", answer)
assert answer == 14208061823964

########
# PART 2

def calc_p2(expression):
    pattern_group = re.compile(r"^(.*)\((.*?)\)(.*)$")
    pattern_simple1 = re.compile(r"^(.*?)(\d+ [+] \d+)(.*)$")
    pattern_simple2 = re.compile(r"^(\d+ [*] \d+)(.*)$")

    while True:
        m = pattern_group.match(expression)
        if m:
            expression = m.group(1) + str(calc_p2(m.group(2))) + m.group(3)
        else:
            break

    while True:
        m = pattern_simple1.match(expression)
        if m:
            expression = m.group(1) + str(eval(m.group(2))) + m.group(3)
        else:
            break

    while True:
        m = pattern_simple2.match(expression)
        if m:
            expression = str(eval(m.group(1))) + m.group(2)
        else:
            break

    return eval(expression)


# 1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
assert calc_p2("1 + (2 * 3) + (4 * (5 + 6))") == 51
# 2 * 3 + (4 * 5) becomes 46.
assert calc_p2("2 * 3 + (4 * 5)") == 46
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
assert calc_p2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
assert calc_p2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
assert calc_p2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


lines = []
with open("event2020/day18/input.txt", "r") as file:
    for line in file:
        lines.append(calc_p2(line[:-1]))

answer = sum(lines)
print("Part 2 =", answer)
assert answer == 320536571743074
