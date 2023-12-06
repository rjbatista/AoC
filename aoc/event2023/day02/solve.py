""" Advent of code 2023 - day 02 """
from functools import reduce
from pathlib import Path
import re

########
# PART 1

type GameSet = dict[str, int]
type Game = tuple[int, list[GameSet]]


def read(filename: str) -> list[Game]:
    """ Read the file """
    game_regex = re.compile(r'Game (\d+): (.*)')

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        games = []
        for line in file:
            m = game_regex.match(line)
            game_id = int(m[1])
            set_parts = m[2].split('; ')

            draws = []
            for s in set_parts:
                cubes = {}
                for cube_parts in s.split(', '):
                    parts = cube_parts.split(' ')
                    cubes[parts[1]] = int(parts[0])
                draws.append(cubes)

            games.append((game_id, draws))

        return games


# loaded with 12 red cubes, 13 green cubes, and 14 blue cubes
BAG: GameSet = {'red': 12, 'green': 13, 'blue': 14}


def filter_for_bag(game: Game) -> bool:
    """ Filter games that cannot be done with BAG """

    for draw in game[1]:
        for color, no in BAG.items():
            if draw.get(color, 0) > no:
                return False

    return True


ex1 = read("example1.txt")
assert sum(game[0] for game in filter(filter_for_bag, ex1)) == 8

inp = read("input.txt")
ANSWER = sum(game[0] for game in filter(filter_for_bag, inp))
print("Part 1 =", ANSWER)
assert ANSWER == 2204  # check with accepted answer

########
# PART 2


def get_minimum_bag(game: Game) -> GameSet:
    """ Gets the minimum bag for game """
    min_bag = {}
    for draw in game[1]:
        for color, no in draw.items():
            min_bag[color] = max(min_bag.get(color, 0), no)

    return min_bag


def power(bag: GameSet):
    """ Calculates the power of the game """
    return reduce(lambda x, y: x * y, bag.values())


assert power(get_minimum_bag(ex1[0])) == 48
assert sum(power(get_minimum_bag(game)) for game in ex1) == 2286


ANSWER = sum(power(get_minimum_bag(game)) for game in inp)
print("Part 2 =", ANSWER)
assert ANSWER == 71036  # check with accepted answer
