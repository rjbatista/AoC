""" Advent of code 2023 - day 19 """
from pathlib import Path
import re

########
# PART 1

# idx, operator, value, dest
type Rule = tuple[int, str, int, str]
# list, default
type Workflow = tuple[list[Rule], str]
# name, workflow
type Workflows = dict[str, Workflow]
# x, m, a, s
type Part = tuple[int, int, int, int]

CATEGORIES = {'x': 0, 'm': 1, 'a': 2, 's': 3}


def read(filename: str) -> tuple[Workflows, list[Part]]:
    """ Read the file """

    def _read_workflow(file):
        parse_expr = re.compile(r'^(\w+){(.*)}$')
        rule_expr = re.compile(r'(\w+)([<>])(\d+):(\w+)')
        workflows = {}
        while True:
            line = file.readline().strip()
            if not line:
                break

            m = parse_expr.match(line)
            if m:
                name, rules = m.groups()

                rules = rules.split(',')
                default = rules[-1]
                workflow_list = []
                for rule in rules[:-1]:
                    m = rule_expr.match(rule)
                    if m:
                        workflow_list.append((CATEGORIES[m[1]], m[2], int(m[3]), m[4]))
                    else:
                        raise RuntimeError("Invalid input")

                workflows[name] = (workflow_list, default)
            else:
                raise RuntimeError("Invalid input")

        return workflows

    def _read_parts(file):
        parse_expr = re.compile(r'^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$')
        parts = []
        while True:
            line = file.readline().strip()
            if not line:
                break

            m = parse_expr.match(line)
            if m:
                parts.append(tuple(int(x) for x in m.groups()))
            else:
                raise RuntimeError("Invalid input")

        return parts

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return _read_workflow(file), _read_parts(file)


def is_accepted(workflows: Workflows, part: Part):
    """ Check if a part is accepted """
    cur = 'in'
    while cur not in ['A', 'R']:
        rules, default = workflows[cur]
        applied_rule = False
        for idx, operator, value, dest in rules:
            if (operator == '<' and part[idx] < value or operator == '>' and part[idx] > value):
                cur = dest
                applied_rule = True
                break

        if not applied_rule:
            cur = default

    return cur == 'A'


def get_accepted_parts(workflows: Workflows, parts: list[Part]):
    """ return the accepted parts """
    return (part for part in parts if is_accepted(workflows, part))


ex1 = read("example1.txt")
assert sum(sum(x) for x in get_accepted_parts(*ex1)) == 19114

inp = read("input.txt")
ANSWER = sum(sum(x) for x in get_accepted_parts(*inp))
print("Part 1 =", ANSWER)
assert ANSWER == 401674  # check with accepted answer

########
# PART 2


def get_total_combinations(workflows: Workflows):
    """ return the total number of combinations accepted """

    def _count(ranges: tuple[tuple[int, int], ...]):
        total = 1
        for low, high in ranges:
            total *= high - low + 1
        return total

    total_accepted = 0
    todo = [('in', ((1, 4000), (1, 4000), (1, 4000), (1, 4000)))]
    while todo:
        cur, ranges = todo.pop()

        if cur == 'A':
            total_accepted += _count(ranges)
            continue

        if cur == 'R':
            continue

        rules, default = workflows[cur]
        done = False
        for idx, operator, value, dest in rules:
            min_v, max_v = ranges[idx]

            if operator == '>':
                new_min_v = value + 1
                new_max_v = max_v
                max_v = value
            else:
                new_min_v = min_v
                new_max_v = value - 1
                min_v = value

            if new_max_v - new_min_v > 0:
                todo.append((dest, ranges[:idx] + ((new_min_v, new_max_v),) + ranges[idx + 1:]))

            if max_v - min_v > 0:
                ranges = ranges[:idx] + ((min_v, max_v),) + ranges[idx + 1:]
            else:
                done = True
                break

        if not done:
            todo.append((default, ranges))

    return total_accepted


assert get_total_combinations(ex1[0]) == 167409079868000


ANSWER = get_total_combinations(inp[0])
print("Part 2 =", ANSWER)
assert ANSWER == 134906204068564  # check with accepted answer
