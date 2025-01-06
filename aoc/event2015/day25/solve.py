""" Advent of code 2015 - day 25 """

########
# PART 1


def find_code(row: int, col: int) -> int:
    """ Find the code for the row, col """
    firstcode = 20151125
    base = 252533
    mod = 33554393
    diagonal = row + col - 1
    exp = diagonal * (diagonal - 1) // 2 + col - 1

    return pow(base, exp, mod) * firstcode % mod


answer = find_code(row=2981, col=3075)
print("Part 1 =", answer)
assert answer == 9132360  # check with accepted answer
