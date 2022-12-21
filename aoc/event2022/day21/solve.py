""" Advent of code 2022 - day 21 without eval :) """
from pathlib import Path
import re

########
# PART 1

OPERATIONS = {
    '+': lambda a, b : a + b,
    '*': lambda a, b : a * b,
    '-': lambda a, b : a - b,
    '/': lambda a, b : a // b
}


def read(filename: str) -> list:
    """ Read the file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        pattern = re.compile(r"^(\w+): (?:(\d+)|(?:(\w+) ([/*+-]) (\w+)))$")

        known = {}
        expressions = {}
        dependants = {}
        for line in file:
            match = pattern.match(line)
            if match:
                if match[2] is not None:
                    known[match[1]] = int(match[2])
                else:
                    expressions[match[1]] = match[3], match[4], match[5], 2

                    dependants.setdefault(match[3], set()).add(match[1])
                    dependants.setdefault(match[5], set()).add(match[1])
            else:
                raise RuntimeError("invalid line: " + line)

        return known, expressions, dependants


def resolve(known, expressions, dependants):
    """
    Resolve the expressions and return the result for 'root'.
    Preparing for part 2, update the possible ones and return None if 'root' is unresolvable
    """
    todo = list(known.keys())

    for key in todo:
        if key in dependants:
            for dependant in dependants[key]:
                left, operation, right, unknowns = expressions[dependant]
                unknowns -= 1

                if left == key:
                    left = known[key]
                elif right == key:
                    right = known[key]

                if unknowns == 0:
                    known[dependant] = OPERATIONS[operation](left, right)
                    todo.append(dependant)
                else:
                    expressions[dependant] = left, operation, right, unknowns

    return known['root'] if 'root' in known else None


ex1 = read("example1.txt")
assert resolve(*ex1) == 152

inp = read("input.txt")
ANSWER = resolve(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 194058098264286 # check with accepted answer

########
# PART 2

INVERSE_OPERATION_LEFT = {
    '+': lambda e, a : e - a,
    '*': lambda e, a : e // a,
    '-': lambda e, a : a - e,
    '/': lambda e, a : a // e
}
INVERSE_OPERATION_RIGHT = {
    '+': lambda e, a : e - a,
    '*': lambda e, a : e // a,
    '-': lambda e, a : e + a,
    '/': lambda e, a : e * a
}


def read_with_correction(filename):
    """ Read the file and apply the "corrections" """
    known, expressions, dependants = read(filename)

    # remove humn
    known.pop('humn')

    # correct root
    left, operation, right, unknowns = expressions['root']
    expressions['root'] = left, operation, right, unknowns

    return known, expressions, dependants


def resolve_p2(known, expressions, dependants):
    """ Resolve finding the unknown 'humn' """
    resolve(known, expressions, dependants)

    left, _, right, _ = expressions['root']
    expression, cur = (left, right) if isinstance(left, int) else (right, left)

    while cur != 'humn':
        left, operation, right, _ = expressions[cur]

        if isinstance(left, int):
            # right is unknown
            expression = INVERSE_OPERATION_LEFT[operation](expression, left)
            cur = right
        else:
            # left is unknown
            expression = INVERSE_OPERATION_RIGHT[operation](expression, right)
            cur = left

    return expression


ex1 = read_with_correction("example1.txt")
assert resolve_p2(*ex1) == 301

inp = read_with_correction("input.txt")
ANSWER = resolve_p2(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 3592056845086 # check with accepted answer
