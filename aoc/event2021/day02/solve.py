import re

########
# PART 1

def read(filename):
    """ parse the input """
    with open("event2021/day02/" + filename, "r") as file:
        pattern = re.compile(r"(\w+) (\d+)")

        actions = []
        for line in file:
            match = pattern.match(line)
            if match:
                actions += [(match.group(1), int(match.group(2)))]
            else:
                raise RuntimeError("invalid input " + line)

    return actions


def run_actions(actions):
    pos = 0
    depth = 0

    for action, value in actions:
        if action == "forward":
            pos += value
        elif action == "up":
            depth -= value
        elif action == "down":
            depth += value

    return pos * depth


# example 1
ex1 = read("example1.txt")
assert run_actions(ex1) == 150

inp = read("input.txt")
answer = run_actions(inp)
print("Part 1 =", answer)
assert answer == 2117664 # check with accepted answer


########
# PART 2

def run_actions_with_aim(actions):
    aim = 0
    pos = 0
    depth = 0

    for action, value in actions:
        if action == "forward":
            pos += value
            depth += aim * value
        elif action == "up":
            aim -= value
        elif action == "down":
            aim += value

    return pos * depth


assert run_actions_with_aim(ex1) == 900


answer = run_actions_with_aim(inp)
print("Part 2 =", answer)
assert answer == 2073416724 # check with accepted answer
