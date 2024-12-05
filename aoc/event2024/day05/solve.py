""" Advent of code 2024 - day 05 """

from pathlib import Path
from collections import defaultdict

########
# PART 1

type Rules = dict[int, list[int]]
type Update = tuple[int]

def read(filename: str) -> tuple[Rules, list[Update]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        line = file.readline().strip()
        rules = defaultdict(list)
        while line:
            before, after = map(int, line.split("|"))

            rules[before].append(after)

            line = file.readline().strip()

        updates = []
        for line in file:
            update = tuple(map(int, line.strip().split(',')))

            assert len(update) % 2 == 1

            updates.append(update)

        return rules, updates


def is_valid(rules: Rules, update: Update) -> bool:
    """ Check if an update is valid with the specified rules """

    done = set()
    for page in update:
        rule = rules[page]

        if any(rule_page for rule_page in rule if rule_page in done):
            return False

        done.add(page)

    return True


def sum_middle_of_valid_updates(rules: Rules, updates: list[Update]):
    """ Sum the middle page of all the valid updates """

    return sum(update[len(update) // 2] for update in updates if is_valid(rules, update))


ex1 = read("example1.txt")
assert sum_middle_of_valid_updates(*ex1) == 143

inp = read("input.txt")
ANSWER = sum_middle_of_valid_updates(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 5452  # check with accepted answer

########
# PART 2

def correct_update(rules: Rules, update: Update) -> Update:
    """ Correct the update acording to the specified rules """

    done = {}
    for idx, page in enumerate(update):
        rule = rules[page]

        fail_idx = next((done[rule_page] for rule_page in rule if rule_page in done), None)

        if fail_idx is not None:
            new_update = list(update)

            new_update[idx], new_update[fail_idx] = new_update[fail_idx], new_update[idx]

            return correct_update(rules, new_update)

        done[page] = idx

    return update


def sum_middle_of_corrected_invalid_updates(rules: Rules, updates: list[Update]):
    """ Sum the middle page of all the invalid updates after correction """

    return sum(correct_update(rules, update)[len(update) // 2]
                for update in updates if not is_valid(rules, update))


assert sum_middle_of_corrected_invalid_updates(*ex1) == 123

ANSWER = sum_middle_of_corrected_invalid_updates(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 4598  # check with accepted answer
