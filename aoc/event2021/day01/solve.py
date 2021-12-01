########
# PART 1

def read(filename):
    """ parse the input """
    with open("event2021/day01/" + filename, "r") as file:
        depths = [int(x[:-1]) for x in file.readlines()]

    return depths


def calc_increases(depths):
    """ calculate the increases """
    return sum([1 for x, y in zip(depths, depths[1:]) if y > x])


# example 1
ex1 = read("example1.txt")
assert calc_increases(ex1) == 7

inp = read("input.txt")
answer = calc_increases(inp)
print("Part 1 =", answer)
assert answer == 1754 # check with accepted answer


########
# PART 2

def sliding_windows(depths):
    """ calculate the sums of the sliding windows """
    return [sum(x) for x in zip(depths, depths[1:], depths[2:])]


assert calc_increases(sliding_windows(ex1)) == 5

answer = calc_increases(sliding_windows(inp))
print("Part 2 =", answer)
assert answer == 1789 # check with accepted answer
