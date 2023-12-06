""" Advent of code 2023 - day 04 """
from collections import defaultdict
from pathlib import Path
import re

########
# PART 1

type Cards = dict[int, tuple[set[int], set[int]]]


def read(filename: str) -> Cards:
    """ Read the file """
    line_regex = re.compile(r'^Card\s+(\d+): ((?:\s*\d+)+)\s*\|\s*((?:\s*\d+)+)$')
    numbers_regex = re.compile(r'\d+')

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        cards = {}
        for line in file:
            m = line_regex.match(line)
            if m:
                winning = set(map(int, numbers_regex.findall(m[2])))
                have = set(map(int, numbers_regex.findall(m[3])))

                cards[int(m[1])] = winning, have
            else:
                raise RuntimeError("invalid input " + line)

        return cards


def score(winning: set[int], have: set[int]) -> int:
    """ Calculate score for a card """
    hits = len(have.intersection(winning))

    return 2 ** (hits - 1) if hits > 0 else 0


ex1 = read("example1.txt")

assert sum(score(winning, have) for (winning, have) in ex1.values()) == 13

inp = read("input.txt")

ANSWER = sum(score(winning, have) for (winning, have) in inp.values())
print("Part 1 =", ANSWER)
assert ANSWER == 25571  # check with accepted answer

########
# PART 2


def count_total_cards(cards: Cards) -> int:
    """ Count the total number of cards """
    count = defaultdict(lambda: 1)
    todo = list(range(1, len(cards) + 1))

    while todo:
        card = todo.pop(0)
        no = count[card]
        winning, have = cards[card]

        hits = len(have.intersection(winning))
        for i in range(hits):
            count[card + i + 1] += no

    return sum(count.values())


assert count_total_cards(ex1) == 30

ANSWER = count_total_cards(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 8805731  # check with accepted answer
