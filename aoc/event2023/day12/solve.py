""" Advent of code 2023 - day 12 """
import functools
from pathlib import Path

########
# PART 1

type Groups = tuple[int, ...]
type Record = tuple[str, Groups]


def read(filename: str) -> list[Record]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [(part[0], tuple(map(int, part[1].split(','))))
                for part in (line.split() for line in file)]


def count_arrangements(record: Record) -> int:
    """ Find the possible arrangements for record """
    @functools.cache
    def _count_arrangements(record: Record, avail: int,
                            cond_pos: int, expect_pos: int, run: int):

        condition, expected = record

        if cond_pos == len(condition):
            if run > 0:
                if expected[expect_pos] != run:
                    return 0

                expect_pos += 1
                run = 0

            if run == 0 and expect_pos == len(expected):
                return 1

            return 0

        total = 0
        if condition[cond_pos] == '?':
            if run > 0 and expected[expect_pos] == run:
                # end the current run
                total += _count_arrangements(record, avail, cond_pos + 1, expect_pos + 1, 0)
            elif run == 0:
                total += _count_arrangements(record, avail, cond_pos + 1, expect_pos, run)

            if avail:
                total += _count_arrangements(record, avail - 1, cond_pos + 1, expect_pos, run + 1)
        elif condition[cond_pos] == '#':
            total = _count_arrangements(record, avail, cond_pos + 1, expect_pos, run + 1)
        else:
            if run > 0:
                # end the current run
                if expected[expect_pos] != run:
                    return 0
                expect_pos += 1
                run = 0

            total = _count_arrangements(record, avail, cond_pos + 1, expect_pos, run)

        return total

    condition, expected = record
    avail = sum(expected) - sum(1 for ch in condition if ch == '#')

    return _count_arrangements(record, avail, 0, 0, 0)


ex1 = read("example1.txt")
assert sum(count_arrangements(x) for x in ex1) == 21

inp = read("input.txt")
ANSWER = sum(count_arrangements(x) for x in inp)
print("Part 1 =", ANSWER)
assert ANSWER == 8022  # check with accepted answer


########
# PART 2

def fold(record: Record) -> Record:
    """ Fold the record """

    condition, expected = record

    return '?'.join([condition] * 5), tuple(expected * 5)


assert sum(count_arrangements(fold(x)) for x in ex1) == 525152

ANSWER = sum(count_arrangements(fold(x)) for x in inp)
print("Part 2 =", ANSWER)
assert ANSWER == 4968620679637  # check with accepted answer
