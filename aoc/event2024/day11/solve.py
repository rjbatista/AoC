""" Advent of code 2024 - day 11 """

from collections import Counter
from math import floor, log10
from pathlib import Path


########
# PART 1


def read(filename: str) -> list[int]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return list(map(int, file.readline().split()))


def blink_item(stone: int) -> list[int]:
    """ blink one stone """
    if stone == 0:
        return [1]

    length = floor(log10(stone)) + 1

    if length % 2 == 0:
        middle = 10 ** ((length // 2))

        return [stone // middle, stone % middle]

    return [stone * 2024]


def blink(stones: list[int]):
    """ simulate a blink """
    out = []
    for stone in stones:
        out += blink_item(stone)

    return out


ex1 = read("example1.txt")
assert blink(ex1) == [1, 2024, 1, 0, 9, 9, 2021976]

ex2 = read("example2.txt")
for i in range(1, 26):
    ex2 = blink(ex2)
    if i == 1:
        # After 1 blink:
        assert ex2 == [253000, 1, 7]
    elif i == 2:
        # After 2 blinks:
        assert ex2 == [253, 0, 2024, 14168]
    elif i == 3:
        # After 3 blinks:
        assert ex2 == [512072, 1, 20, 24, 28676032]
    elif i == 4:
        # After 4 blinks:
        assert ex2 == [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
    elif i == 5:
        # After 5 blinks:
        assert ex2 == [1036288, 7, 2, 20, 24, 4048, 1,
                       4048, 8096, 28, 67, 60, 32]
    elif i == 6:
        # After 6 blinks:
        assert ex2 == [2097446912, 14168, 4048, 2, 0, 2, 4, 40,
                       48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]

assert len(ex2) == 55312

inp = read("input.txt")
for _ in range(25):
    inp = blink(inp)
ANSWER = len(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 186175  # check with accepted answer


########
# PART 2


def blink_with_counter(stones: list[int], times: int) -> int:
    """ simulate blink for several times and return the number of stones """
    counter = Counter(stones)

    for _ in range(times):
        new_counter = Counter()
        for stone, count in counter.items():
            for new_stone in blink_item(stone):
                new_counter[new_stone] += count

        counter = new_counter

    return sum(y for _, y in counter.items())


ex2 = read("example2.txt")
assert blink_with_counter(ex2, 1) == 3
assert blink_with_counter(ex2, 2) == 4
assert blink_with_counter(ex2, 3) == 5
assert blink_with_counter(ex2, 4) == 9
assert blink_with_counter(ex2, 5) == 13
assert blink_with_counter(ex2, 6) == 22
assert blink_with_counter(ex2, 25) == 55312

ANSWER = blink_with_counter(inp, 50)
print("Part 2 =", ANSWER)
assert ANSWER == 220566831337810  # check with accepted answer
