""" Advent of code 2023 - day 22 """

from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

########
# PART 1

Coord = namedtuple("Coord", "x y z")


@dataclass
class Brick:
    """ A Brick """
    id: int
    start: Coord
    end: Coord
    _supported_bricks: dict[int, Self] = field(default_factory=dict)
    _supported_by_bricks: dict[int, Self] = field(default_factory=dict)

    def __post_init__(self):
        # assume ordered points
        for p0, p1 in zip(self.start, self.end):
            assert p0 <= p1

    @property
    def base(self) -> int:
        """ Returns the base height """
        return self.start.z  # z

    @property
    def top(self) -> int:
        """ Returns the top height """
        return self.end.z  # z

    @property
    def no_supporting_bricks(self) -> int:
        """ Returns the number of supported bricks """
        return len(self._supported_by_bricks)

    def is_over_the_same_space(self,  other: Self) -> bool:
        """ check if a Brink is directly under another """
        x1, y1, _ = self.start
        x2, y2, _ = self.end

        x3, y3, _ = other.start
        x4, y4, _ = other.end

        return x2 >= x3 and x1 <= x4 and y2 >= y3 and y1 <= y4

    def add_brick_above(self, brick: Self):
        """ Add a brick above this one """
        self._supported_bricks[brick.id] = brick

    def add_brick_below(self, brick: Self):
        """ Add a brick below this one """
        self._supported_by_bricks[brick.id] = brick

    def settled(self: Self):
        """ Adjust the brick after settled """
        self._supported_bricks = {
            id: brick for id, brick in self._supported_bricks.items() if self._is_below(brick)
        }
        self._supported_by_bricks = {
            id: brick for id, brick in self._supported_by_bricks.items() if self._is_above(brick)
        }

    def _is_above(self, other: Self) -> bool:
        return other.top + 1 == self.base

    def _is_below(self, other: Self) -> bool:
        return self.top + 1 == other.base

    def get_supported_by_bricks(self) -> list['Brick']:
        """ Return bricks that support this one """
        return self._supported_by_bricks.values()

    def get_supported_bricks(self) -> list['Brick']:
        """ Return bricks that are supported by this one """
        return self._supported_bricks.values()

    def lower(self, height: int):
        """ Lower the brick by the specified height """
        self.start = Coord(self.start.x, self.start.y, self.start.z - height)
        self.end = Coord(self.end.x, self.end.y, self.end.z - height)

    def can_disintegrate(self) -> bool:
        """ Check if a brick can be disintegrated """
        for brick in self.get_supported_bricks():
            # cannot if it is only supported by this brick
            if brick.no_supporting_bricks == 1:
                return False

        return True

    def count_fall_on_disintegration(self) -> int:
        """ Count all the bricks that fall with the disintegration of this one """
        todo = [self]
        disintegrated = set([self.id])

        while todo:
            current_brick = todo.pop()
            for supported in current_brick.get_supported_bricks():
                if supported.id in disintegrated:
                    continue

                # check for supporting bricks not disintegrated
                if not any(brick for brick in supported.get_supported_by_bricks()
                           if brick.id not in disintegrated):
                    disintegrated.add(supported.id)

                todo.append(supported)

        return len(disintegrated) - 1

    @staticmethod
    def _settle(bricks: list['Brick']):
        bricks.sort(key=lambda b: b.base)

        for current in bricks:
            if current.base == 1:
                continue

            bricks_below = [brick for brick in bricks if brick.base < current.base]

            if not bricks_below:
                continue

            top_of_bricks_below = 1
            for brick in bricks_below:
                if brick.is_over_the_same_space(current):
                    current.add_brick_below(brick)
                    brick.add_brick_above(current)
                    top_of_bricks_below = max(top_of_bricks_below, brick.top + 1)

            if current.base > top_of_bricks_below:
                current.lower(current.base - top_of_bricks_below)

        for current in bricks:
            current.settled()

    @staticmethod
    def read(filename: str) -> list['Brick']:
        """ Read from a file """

        with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
            bricks = []
            for line_number, line in enumerate(file):
                start, end = (Coord(*map(int, part.split(','))) for part in line.strip().split('~'))
                bricks.append(Brick(line_number, start, end))

        Brick._settle(bricks)

        return bricks


ex1 = Brick.read('example1.txt')
assert sum(1 for b in ex1 if b.can_disintegrate()) == 5

inp = Brick.read('input.txt')
ANSWER = sum(1 for b in inp if b.can_disintegrate())
print("Part 1 =", ANSWER)
assert ANSWER == 465  # check with accepted answer

########
# PART 2

assert sum(b.count_fall_on_disintegration() for b in ex1) == 7

ANSWER = sum(b.count_fall_on_disintegration() for b in inp)
print("Part 2 =", ANSWER)
assert ANSWER == 79042  # check with accepted answer
