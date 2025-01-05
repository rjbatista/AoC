""" Advent of code 2024 - day 25 """

from pathlib import Path

########
# PART 1

type Schematic = list[tuple[int, ...]]


def read(filename: str) -> tuple[Schematic, Schematic]:
    """ Read from a file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        keys = []
        locks = []
        cur_form = []
        is_key = None

        for line in file:
            line = line.strip()

            if not line:
                if is_key:
                    keys.append(tuple(x - 1 for x in cur_form))
                else:
                    locks.append(tuple(cur_form))

                cur_form = None
                is_key = None
                continue

            if is_key is None:
                cur_form = [0] * len(line)
                is_key = line.startswith(".")

                continue

            for i, ch in enumerate(line):
                if ch == '#':
                    cur_form[i] += 1

        if is_key:
            keys.append(tuple(x - 1 for x in cur_form))
        else:
            locks.append(tuple(cur_form))

        return keys, locks


def find_fits(keys: Schematic, locks: Schematic) -> int:
    """ find fits """
    fits = 0
    for key in keys:
        for lock in locks:
            sums = tuple((a + b) for a, b in zip(key, lock))

            if not any(x > 5 for x in sums):
                fits += 1

    return fits


ex1 = read("example1.txt")
assert find_fits(*ex1) == 3

inp = read("input.txt")
ANSWER = find_fits(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 3090  # check with accepted answer
