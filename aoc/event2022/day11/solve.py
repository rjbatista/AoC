""" Advent of code 2022 - day 11 """
from pathlib import Path
import re
from dataclasses import dataclass
from typing import List
from functools import reduce
from operator import mul

########
# PART 1

@dataclass
class Monkey:
    # pylint: disable=too-many-instance-attributes,invalid-name

    """ Monkey class """
    PATTERN_ID = re.compile(r"^Monkey (\d+):$")
    PATTERN_ITEMS = re.compile(r"^\s+Starting items: ((?:\d+(?:, )?)+)$")
    PATTERN_OPERATION = re.compile(r"^\s+Operation: new = (.*)$")
    PATTERN_TEST = re.compile(r"^\s+Test: divisible by (\d+)$")
    PATTERN_DECISION = re.compile(r"\s+If \w+: throw to monkey (\d+)$")

    _group: List['Monkey']
    monkey_id: int
    items: List[int]
    _operation: str
    test_modulus: int
    _true_destination: int
    _false_destination: int
    worry_divider : int
    inspects : int = 0

    def __post_init__(self):
        self._group.append(self)

    def _inspect(self, item, reducer = None):
        """ Inspect an item """
        self.inspects += 1

        # eval is not a good thing to use, but saves a LOT of work here
        new = eval(self._operation, {}, {'old': item}) // self.worry_divider
        if reducer is not None:
            new %= reducer

        if new % self.test_modulus == 0:
            self._group[self._true_destination].items.append(new)
        else:
            self._group[self._false_destination].items.append(new)

    def do_round(self, reducer = None):
        """ Do a round """
        while self.items:
            item = self.items.pop(0)
            self._inspect(item, reducer)


    @staticmethod
    def read_monkey(file, monkeys, worry_divider):
        """ Read monkey from file """
        monkey_id = Monkey.PATTERN_ID.match(file.readline()).group(1)
        items = list(map(int, Monkey.PATTERN_ITEMS.match(file.readline()).group(1).split(",")))
        operation = compile(Monkey.PATTERN_OPERATION.match(file.readline()).group(1),
                filename='no-file.py', mode='eval')
        test = int(Monkey.PATTERN_TEST.match(file.readline()).group(1))
        true_destination = int(Monkey.PATTERN_DECISION.match(file.readline()).group(1))
        false_destination = int(Monkey.PATTERN_DECISION.match(file.readline()).group(1))

        Monkey(monkeys, monkey_id, items, operation, test,
            true_destination, false_destination, worry_divider)

        return file.readline()


def read(filename, worry_divider = 3):
    """ Read all monkeys from file """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        monkeys = []
        while Monkey.read_monkey(file, monkeys, worry_divider):
            pass

        return monkeys


def do_rounds(monkeys, times = 20):
    """ Do times rounds """
    for _ in range(times):
        for monkey in monkeys:
            monkey.do_round()


def calculate_monkey_business(monkeys):
    """ Calculate the monkey business """
    return reduce(mul, sorted([monkey.inspects for monkey in monkeys], reverse = True)[:2])


ex1 = read("example1.txt")
do_rounds(ex1)
assert calculate_monkey_business(ex1) == 10605

inp = read("input.txt")
do_rounds(inp)
ANSWER = calculate_monkey_business(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 72884 # check with accepted answer

########
# PART 2

def do_rounds_with_reducer(monkeys, times = 10000):
    """ Do rounds using a reducer """
    reducer = reduce(mul, [monkey.test_modulus for monkey in monkeys])

    for _ in range(times):
        for monkey in monkeys:
            monkey.do_round(reducer)


ex1 = read("example1.txt", 1)
do_rounds_with_reducer(ex1)
assert calculate_monkey_business(ex1) == 2713310158

inp = read("input.txt", 1)
do_rounds_with_reducer(inp)

ANSWER = calculate_monkey_business(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 15310845153 # check with accepted answer
