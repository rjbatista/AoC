""" Advent of code 2022 - day 01 """
from pathlib import Path

########
# PART 1

def read(filename):
    """ read input """
    elves = [[]]
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line in file.readlines():
            if len(line.strip()) == 0:
                elves += [[]]
            else:
                elves[-1] += [int(line)]

    return elves


ex1 = read("example1.txt")
assert max([sum(x) for x in ex1]) == 24000

inp = read("input.txt")
answer = max([sum(x) for x in inp])
print("Part 1 =", answer)
assert answer == 75622 # check with accepted answer

########
# PART 2

assert sum(sorted([sum(x) for x in ex1], reverse=True)[0:3]) == 45000

answer = sum(sorted([sum(x) for x in inp], reverse=True)[0:3])
print("Part 2 =", answer)
assert answer == 213159 # check with accepted answer
