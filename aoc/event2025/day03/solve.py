""" Advent of code 2025 - day 03 """

from pathlib import Path

########
# PART 1


def read(filename: str) -> list[tuple[int, int]]:
    """ Read from a file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [list(int(battery) for battery in bank.strip()) for bank in file.readlines()]


def max_joltage(bank: list[int], number=2):
    """ find the max joltage in bank """

    if not bank:
        return 0

    avail = bank if number == 1 else bank[:-(number - 1)]

    m = (0, 0)
    for idx, battery in enumerate(avail):
        if battery == 9:
            m = idx, 9
            break

        if battery > m[1]:
            m = idx, battery

    if number > 1:
        return m[1] * 10 ** (number - 1) + max_joltage(bank[m[0] + 1:], number - 1)

    return m[1]


ex1 = read("example1.txt")
assert sum(max_joltage(x) for x in ex1) == 357

inp = read("input.txt")
ANSWER = sum(max_joltage(x) for x in inp)
print("Part 1 =", ANSWER)
assert ANSWER == 17332  # check with accepted answer

########
# PART 2

assert sum(max_joltage(x, 12) for x in ex1) == 3121910778619

ANSWER = sum(max_joltage(x, 12) for x in inp)
print("Part 2 =", ANSWER)
assert ANSWER == 172516781546707  # check with accepted answer
