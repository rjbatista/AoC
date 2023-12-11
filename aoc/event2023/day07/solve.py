""" Advent of code 2023 - day XX """
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering
from pathlib import Path
from typing import Self

########
# PART 1


class HandType(Enum):
    """ The hand type """
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

    def __lt__(self, __o: Self) -> bool:
        return self.value < __o.value


@dataclass
@total_ordering
class Hand:
    """ Class for Camel Cards hand """
    hand: str
    bid: int
    _values: str = field(init=False, repr=False, compare=False)
    _type: HandType = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        translate = str.maketrans("TJQKA", "ABCDE")
        self._values = self.hand.translate(translate)
        self._type = Hand.determine_rank(self.hand)

    def __lt__(self, __o: Self) -> bool:
        return self._type < __o._type if self._type != __o._type else self._values > __o._values

    @classmethod
    def determine_rank(cls, hand: str) -> HandType:
        """ Fill the rank """

        counter = Counter(hand)
        groups = counter.most_common(4)

        if groups[0][1] == 5:
            hand_type = HandType.FIVE_OF_A_KIND
        elif groups[0][1] == 4:
            hand_type = HandType.FOUR_OF_A_KIND
        elif groups[0][1] == 3:
            if groups[1][1] == 2:
                hand_type = HandType.FULL_HOUSE
            else:
                hand_type = HandType.THREE_OF_A_KIND
        elif groups[0][1] == 2:
            if groups[1][1] == 2:
                hand_type = HandType.TWO_PAIR
            else:
                hand_type = HandType.ONE_PAIR
        else:
            hand_type = HandType.HIGH_CARD

        return hand_type


def read(filename: str) -> list[tuple[str, int]]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        hands = []

        for line in file:
            parts = line.split()
            hands.append(Hand(parts[0], int(parts[1])))

        return hands


def calculate_winnings(hands: list[Hand]) -> int:
    """ Calculate the winnings """
    return sum(hand.bid * rank for rank, hand in enumerate(sorted(hands, reverse=True), 1))


ex1 = read("example1.txt")
assert calculate_winnings(ex1) == 6440

inp = read("input.txt")

ANSWER = calculate_winnings(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 251216224  # check with accepted answer

########
# PART 2


@dataclass
@total_ordering
class HandWithJoker(Hand):
    """ Class for Camel Cards hand, with Jokers instead of Jacks """

    def __post_init__(self):
        translate = str.maketrans("TJQKA", "A1CDE")
        self._values = self.hand.translate(translate)

        if self.hand == "JJJJJ":
            self._type = HandType.FIVE_OF_A_KIND
        else:
            counter = Counter(self.hand.replace("J", ""))
            groups = counter.most_common(1)
            best_hand = self.hand.replace("J", groups[0][0])

            self._type = Hand.determine_rank(best_hand)

    @classmethod
    def from_hand(cls, origin: Hand) -> Self:
        """ Create hand with joker from hand """
        return HandWithJoker(origin.hand, origin.bid)


assert calculate_winnings(map(HandWithJoker.from_hand, ex1)) == 5905

ANSWER = calculate_winnings(map(HandWithJoker.from_hand, inp))
print("Part 2 =", ANSWER)
assert ANSWER == 250825971  # check with accepted answer
