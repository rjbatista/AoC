""" Advent of code 2022 - day 05 """
from pathlib import Path
import re
import copy

########
# PART 1

def read(filename):
    """ read input """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        stack_pattern = re.compile(r"\[(\w)\]")
        procedure_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")

        # stacks
        crates = None
        for line in file:
            if crates is None:
                crates = [[] for _ in range(len(line) // 4)]

            if line.strip() == '':
                break

            for crate in stack_pattern.finditer(line):
                crate_pos = crate.start() // 4
                crate_name = crate.group(1)

                crates[crate_pos].insert(0, crate_name)

        # procedure
        procedure = []
        for line in file:
            procedure.append(tuple(map(int, procedure_pattern.match(line).groups())))

    return crates, procedure


def run_procedure(stacks, procedure):
    """ run the procedure on the stack """
    stacks = copy.deepcopy(stacks)
    for num, from_stack, to_stack in procedure:
        for _ in range(num):
            stacks[to_stack - 1].append(stacks[from_stack - 1].pop())

    return stacks


ex1 = read("example1.txt")
assert ''.join((l[-1] for l in run_procedure(*ex1))) == 'CMZ'

inp = read("input.txt")
answer = ''.join((stack[-1] for stack in run_procedure(*inp)))
print("Part 1 =", answer)
assert answer == 'BZLVHBWQF' # check with accepted answer


########
# PART 2

def run_procedure_p2(stacks, procedure):
    """ run the part 2 procedure on the stack """
    stacks = copy.deepcopy(stacks)
    for num, from_stack, to_stack in procedure:
        stacks[to_stack - 1] += stacks[from_stack - 1][-num:]
        stacks[from_stack - 1] = stacks[from_stack - 1][0:-num]

    return stacks


assert ''.join((stack[-1] for stack in run_procedure_p2(*ex1))) == 'MCD'

answer = ''.join((stack[-1] for stack in run_procedure_p2(*inp)))
print("Part 2 =", answer)
assert answer == 'TDGJQTZSL' # check with accepted answer
