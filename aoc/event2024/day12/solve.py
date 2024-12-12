""" Advent of code 2024 - day 12 """

from collections import defaultdict
from itertools import chain
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def read(filename: str) -> dict[Coord, str]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        garden = {}
        for y, line in enumerate(file):
            for x, ch in enumerate(line.strip()):
                garden[(x, y)] = ch

        return garden


def find_plots(garden: dict[Coord, str]) -> list[set[Coord]]:
    """ find all the plots in the garden """
    def get_plot(garden: dict[Coord, str], pos: Coord) -> set[Coord]:
        """ find a plot in the specified position"""
        todo = set([pos])
        visited = set()
        plot = set()
        plot_type = garden[pos]

        while todo:
            cur = todo.pop()
            x, y = cur

            plot.add(cur)
            visited.add(cur)

            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and garden.get((nx, ny), None) == plot_type:
                    todo.add((nx, ny))

        return plot

    todo = set(garden.keys())

    plots = []
    while todo:
        cur = todo.pop()
        plot = get_plot(garden, cur)

        todo = todo.difference(plot)

        plots.append(plot)

    return plots


def perimeter(garden: dict[Coord, str], plot: set[Coord]) -> int:
    """ Calculate the perimeter """
    ret = []
    for x, y in plot:
        plot_type = garden[x, y]

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if garden.get((nx, ny), None) != plot_type:
                ret.append((nx, ny))

    return len(ret)


def calculate_prices(garden: dict[Coord, str], plots: list[set[Coord]]):
    """ Calculate the price of area * perimeter """
    return sum(len(plot) * perimeter(garden, plot) for plot in plots)


ex1 = read("example1.txt")
assert calculate_prices(ex1, find_plots(ex1)) == 140

ex2 = read("example2.txt")
assert calculate_prices(ex2, find_plots(ex2)) == 772

ex3 = read("example3.txt")
assert calculate_prices(ex3, find_plots(ex3)) == 1930

inp = read("input.txt")
ANSWER = calculate_prices(inp, find_plots(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 1518548  # check with accepted answer

########
# PART 2


def sides(garden: dict[Coord, str], plot: set[Coord]) -> int:
    """ Calculate the sides """
    horiz = defaultdict(set)
    vert = defaultdict(set)
    for x, y in plot:
        plot_type = garden[x, y]

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if garden.get((nx, ny), None) != plot_type:
                if dy:
                    horiz[(ny, dy)].add(nx)
                if dx:
                    vert[(nx, dx)].add(ny)

    todo = sorted(horiz.values())
    count = 0
    for line in chain(horiz.values(), vert.values()):
        todo = sorted(line)
        while todo:
            count += 1
            x = todo.pop(0)
            while todo and todo[0] == x + 1:
                x = todo.pop(0)

    return count


def calculate_prices_with_sides(garden: dict[Coord, str], plots: list[set[Coord]]):
    """ Calculate the price of area * sides """
    return sum(len(plot) * sides(garden, plot) for plot in plots)


assert calculate_prices_with_sides(ex1, find_plots(ex1)) == 80
assert calculate_prices_with_sides(ex2, find_plots(ex2)) == 436
ex4 = read("example4.txt")
assert calculate_prices_with_sides(ex4, find_plots(ex4)) == 368
assert calculate_prices_with_sides(ex3, find_plots(ex3)) == 1206


ANSWER = calculate_prices_with_sides(inp, find_plots(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 909564  # check with accepted answer
