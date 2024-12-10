""" Advent of code 2024 - day 10 """

from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
type TopoMap = dict[Coord, int]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def read(filename: str) -> tuple[TopoMap, list[Coord]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        topo_map = {}
        starts = set()
        for y, line in enumerate(file):
            for x, ch in enumerate(line.strip()):
                height = int(ch)

                topo_map[(x, y)] = height
                if height == 0:
                    starts.add((x, y))

        return topo_map, starts


def count_trailheads(topo_map: TopoMap, starts: list[Coord]) -> int:
    """ Find all the trailheads"""

    todo = [(0, x, y, x, y) for x, y in starts]
    count_ends = {}
    count_trails = {}

    while todo:
        current, x, y, sx, sy = todo.pop()
        next_value = current + 1

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            if topo_map.get((nx, ny), 0) == next_value:
                if next_value == 9:
                    count_ends.setdefault((sx, sy), set()).add((nx, ny))
                    count_trails[(sx, sy)] = count_trails.get((sx, sy), 0) + 1
                    continue

                todo.append((next_value, nx, ny, sx, sy))

    return sum(len(ends) for ends in count_ends.values()), sum(count_trails.values())


ex1 = read("example1.txt")
assert count_trailheads(*ex1) == (36, 81)

inp = read("input.txt")
ANSWER = count_trailheads(*inp)
print("Part 1 =", ANSWER[0])
assert ANSWER[0] == 582  # check with accepted answer

########
# PART 2

print("Part 2 =", ANSWER[1])
assert ANSWER[1] == 1302  # check with accepted answer
