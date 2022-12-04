""" Advent of code 2022 - day XX """
from pathlib import Path

########
# PART 1

class Range:
    """ defines a range """
    def __init__(self, start, end):
        self.start = start
        self.end = end


    def __len__(self):
        return self.end - self.start + 1


    def __str__(self):
        rep = ""
        for i in range(10):
            rep += str(i) if self.start <= i <= self.end else '.'

        return rep


    def __repr__(self) -> str:
        return str(self)


    def __contains__(self, another):
        return self.start <= another.start and self.end >= another.end


    def overlaps(self, another):
        """ checks if the range overlaps another """
        return self.start <= another.end and self.end >= another.start



def read(filename):
    """ read input """
    pairs = []
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line in file:
            line = line.strip().split(',')

            pairs.append(tuple(map(lambda x : Range(*(map(int, x.split('-')))), line)))

    return pairs


ex1 = read("example1.txt")
assert (sum([1 for r1, r2 in ex1 if r1 in r2 or r2 in r1])) == 2

inp = read("input.txt")
answer = sum([1 for r1, r2 in inp if r1 in r2 or r2 in r1])
print("Part 1 =", answer)
assert answer == 547 # check with accepted answer

########
# PART 2

assert (sum([1 for r1, r2 in ex1 if r1.overlaps(r2)])) == 4

answer = sum([1 for r1, r2 in inp if r1.overlaps(r2)])
print("Part 2 =", answer)
assert answer == 843 # check with accepted answer
