""" Advent of code 2025 - day 05 """

from pathlib import Path

type Range = tuple[int, int]

########
# PART 1


def read(filename: str) -> tuple[list[Range], list[int]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        ranges = []
        while True:
            line = file.readline().strip()

            if not line:
                break

            ranges.append(tuple(map(int, line.split('-'))))

        ingredients = [int(line.strip()) for line in file]

        return ranges, ingredients


def is_fresh(ranges: list[Range], ingredient: int) -> bool:
    """ check if an ingredient is fresh """
    for start, end in ranges:
        if start <= ingredient <= end:
            return True

    return False


def find_fresh(ranges: list[Range], ingredients: list[int]) -> list[int]:
    """ find the fresh ingredients """

    return [ingredient for ingredient in ingredients if is_fresh(ranges, ingredient)]


ex1 = read("example1.txt")
assert find_fresh(*ex1) == [5, 11, 17]

inp = read("input.txt")
ANSWER = len(find_fresh(*inp))
print("Part 1 =", ANSWER)
assert ANSWER == 640  # check with accepted answer

########
# PART 2


def merge_ranges(ranges: list[Range]) -> list[Range]:
    """ merge the ranges into a list with non-overlapping ranges """

    todo = ranges.copy()
    done = []

    while todo:
        cur_s, cur_e = todo.pop()
        cur_done = True

        for idx, (s, e) in enumerate(todo):
            if cur_s <= e and cur_e >= s:
                n_s = min(cur_s, s)
                n_e = max(cur_e, e)

                todo[idx] = n_s, n_e
                cur_done = False
                break

        if cur_done:
            done.append((cur_s, cur_e))

    return done


assert sum(e - s + 1 for s, e in merge_ranges(ex1[0])) == 14

ANSWER = sum(e - s + 1 for s, e in merge_ranges(inp[0]))
print("Part 2 =", ANSWER)
assert ANSWER == 365804144481581  # check with accepted answer
