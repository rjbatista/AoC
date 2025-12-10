""" Advent of code 2025 - day 07 """

from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]


def read(filename: str) -> tuple[set[Coord], int, Coord]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        diagram = set()

        for y, line in enumerate(file):
            for x, ch in enumerate(line):
                match ch:
                    case '^':
                        diagram.add((x, y))
                    case 'S':
                        start = x, y

            height = y

        return diagram, height, start


def count_splits(diagram: set[Coord], height: int, start: Coord) -> int:
    """ count the times the beam is split """
    count = 0
    beams = [start]
    visited = set()
    while beams:
        x, y = beams.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if (x, y) in diagram:
            # found splitter

            count += 1

            beams.append((x - 1, y))
            beams.append((x + 1, y))
            continue

        if y < height:
            beams.append((x, y + 1))

    return count


ex1 = read("example1.txt")
assert count_splits(*ex1) == 21

inp = read("input.txt")
ANSWER = count_splits(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 1524  # check with accepted answer

########
# PART 2


def count_timelines(diagram: set[Coord], height: int, start: Coord) -> int:
    """ count the times the beam is split """
    def walk(pos: Coord) -> int:
        x, y = pos
        while y < height:
            if (x, y) in known:
                return known[x, y]

            if (x, y) in diagram:
                # found splitter
                v = walk((x - 1, y)) + walk((x + 1, y))

                known[x, y] = v

                return v

            y += 1

        return 1

    known = {}
    return walk(start)


assert count_timelines(*ex1) == 40

ANSWER = count_timelines(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 32982105837605  # check with accepted answer
