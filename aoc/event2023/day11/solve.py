""" Advent of code 2023 - day 11 """
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]


@dataclass
class ExpandedUniverse():
    """ Class representing an expanding universe """

    galaxies: dict[int, Coord] = field(init=False)
    len_x: int = 0
    len_y: int = 0
    extra_per_space: int = 1

    _original_galaxies: dict[int, Coord] = field(init=False)
    _len_x: int = None
    _len_y: int = None

    def read(self, filename: str) -> None:
        """ Read the universe from a file """

        with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
            self._original_galaxies = {}
            max_x = 0
            max_y = 0
            galaxy_id = 0

            for y, line in enumerate(file):
                max_y = max(y, max_y)
                for x, val in enumerate(line.strip()):
                    max_x = max(x, max_x)

                    if val == '#':
                        self._original_galaxies[galaxy_id] = x, y
                        galaxy_id += 1

            self._len_x = max_x + 1
            self._len_y = max_y + 1

        self._expand()

    def update_expansion_factor(self, new_factor: int) -> None:
        """ Updates the expansion factor """
        self.extra_per_space = new_factor - 1

        self._expand()

    def _expand(self) -> None:
        """ Expand empty space """
        galaxy_positions = set(self._original_galaxies.values())
        horizontal_expansions = set()
        vertical_expansions = set()

        empty_cols = [True] * self._len_x
        for y in range(self._len_y):
            empty_row = True
            for x in range(self._len_x):
                if (x, y) in galaxy_positions:
                    empty_row = False
                    empty_cols[x] = False

            if empty_row:
                horizontal_expansions.add(y)

        for x, is_empty in enumerate(empty_cols):
            if is_empty:
                vertical_expansions.add(x)

        self.galaxies = {}
        for galaxy_id, (x, y) in self._original_galaxies.items():
            x_expansions = sum((1 for ex in vertical_expansions if ex < x))
            y_expansions = sum((1 for ey in horizontal_expansions if ey < y))

            self.galaxies[galaxy_id] = (x + x_expansions * self.extra_per_space,
                                        y + y_expansions * self.extra_per_space)

        self.len_x = self._len_x + len(vertical_expansions) * self.extra_per_space
        self.len_y = self._len_y + len(horizontal_expansions) * self.extra_per_space

    def draw(self) -> None:
        """ Draws the expanded map """
        galaxy_positions = set(self.galaxies.values())

        for y in range(self.len_y):
            for x in range(self.len_x):
                if (x, y) in galaxy_positions:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def distances(self) -> list[tuple[int, int, int]]:
        """ Calculate the distances between galaxies """
        galaxies = self.galaxies.items()

        return [(g_id1, g_id2, abs(x2 - x1) + abs(y2 - y1))
                for (g_id1, (x1, y1)), (g_id2, (x2, y2)) in combinations(galaxies, 2)]


ex1 = ExpandedUniverse()
ex1.read("example1.txt")
assert sum(d for _, _, d in ex1.distances()) == 374

inp = ExpandedUniverse()
inp.read("input.txt")

ANSWER = sum(d for _, _, d in inp.distances())
print("Part 1 =", ANSWER)
assert ANSWER == 9214785  # check with accepted answer

########
# PART 2

ex1.update_expansion_factor(10)
assert sum(d for _, _, d in ex1.distances()) == 1030
ex1.update_expansion_factor(100)
assert sum(d for _, _, d in ex1.distances()) == 8410

inp.update_expansion_factor(1000000)
ANSWER = sum(d for _, _, d in inp.distances())
print("Part 2 =", ANSWER)
assert ANSWER == 613686987427  # check with accepted answer
