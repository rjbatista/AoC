""" Advent of code 2022 - day 03 """
from pathlib import Path

########
# PART 1

def read(filename):
    """ read input """
    rucksacks = []
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line in file:
            line = line.strip()
            middle = len(line) // 2

            rucksacks.append((line[:middle], line[middle:]))

    return rucksacks


def find_match_priority(*rucksacks):
    """ find matching element in rucksacks and return its priority """

    ruckset = set(rucksacks[0])
    for rucksack in rucksacks[1:]:
        ruckset = ruckset.intersection(set(rucksack))

    assert len(ruckset) == 1

    match = ruckset.pop()

    return ord(match) - ord('a') + 1 if match.islower() else ord(match) - ord('A') + 27


ex1 = read("example1.txt")
assert sum([find_match_priority(*rucksacks) for rucksacks in ex1]) == 157

inp = read("input.txt")
answer = sum([find_match_priority(*rucksacks) for rucksacks in inp])
print("Part 1 =", answer)
assert answer == 7967 # check with accepted answer

########
# PART 2

def read_p2(filename):
    """ read input, grouping by three """

    with Path(__file__).parent.joinpath(filename).open("r") as file:
        rucksacks = [line.strip() for line in file.readlines()]

        rucksacks = list(zip(rucksacks[::3], rucksacks[1::3], rucksacks[2::3]))

    return rucksacks


ex1 = read_p2("example1.txt")
assert sum([find_match_priority(*rucksacks) for rucksacks in ex1]) == 70

inp = read_p2("input.txt")
answer = sum([find_match_priority(*rucksacks) for rucksacks in inp])
print("Part 2 =", answer)
assert answer == 2716 # check with accepted answer
