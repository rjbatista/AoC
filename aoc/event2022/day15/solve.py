""" Advent of code 2022 - day 15 """
from pathlib import Path
import re

########
# PART 1

def manhattan_distance(p1_x : int, p1_y : int, p2_x : int, p2_y : int) -> int:
    """ calculate the manhattan distance """
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def read(filename):
    """ read sensor information """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        sensor_pattern = re.compile(r"^.* x=(-?\d+), y=(-?\d+): .* x=(-?\d+), y=(-?\d+)$")

        sensors = []
        beacons = set()
        for line_number, line in enumerate(file):
            match = sensor_pattern.match(line)
            if match:
                sensor = (int(match[1]), int(match[2]))
                beacon = (int(match[3]), int(match[4]))

                sensors.append((sensor, manhattan_distance(*beacon, *sensor), beacon))
                beacons.add(beacon)

            else:
                raise RuntimeError(f"Invalid input on line {line_number + 1}: {line}")

        return sensors, beacons


def count_impossible_positions(sensors, beacons, pos_y) -> int:
    """ Count the impossible positions of a specific row """
    impossible = []
    for sensor, distance, _ in sensors:
        s_x, s_y = sensor
        relevant_distance = distance - abs(s_y - pos_y)

        if relevant_distance > 0:
            impossible.append((s_x - relevant_distance, s_x + relevant_distance))

    impossible.sort()

    # merge blocks of impossibles
    pos = 0
    while pos < len(impossible) - 1:
        r1_start, r1_end = impossible[pos]
        r2_start, r2_end = impossible[pos + 1]

        if r1_end >= r2_start:
            impossible[pos] = (r1_start, max(r1_end, r2_end))
            del impossible[pos + 1]
        else:
            pos += 1

    count = sum([end - start + 1 for start, end in impossible])

    for _, beacon_y in beacons:
        if beacon_y == pos_y:
            count -= 1

    return count, impossible


ex1 = read("example1.txt")
assert count_impossible_positions(*ex1, 10)[0] == 26

inp = read("input.txt")
ANSWER = count_impossible_positions(*inp, 2000000)[0]
print("Part 1 =", ANSWER)
assert ANSWER == 5564017 # check with accepted answer


########
# PART 2

MAX_COORD=4000000

def find_distress_signal(sensors, beacons, max_x = MAX_COORD, max_y = MAX_COORD):
    """ Find the distress signal from 0, 0 to max_x, max_y """
    # the direction of search is irrelevant for the general case, but in my input is
    # just quicker reversed, 'cause I've already tested it and it's closer to the end
    # -- a better solution would be to cut the signal areas and consider the areas around
    # the signal areas, but this solution was just faster to implement after part 1

    for pos_y in range(max_y, 0, -1):
        impossible = count_impossible_positions(sensors, beacons, pos_y)[1]

        for (start1 , end1), (start2, end2) in zip(impossible, impossible[1:]):
            if start1 < max_x and end2 > 0:
                gap_start = max(0, end1 + 1)
                gap_end = min(max_x, start2 - 1)

                if gap_end - gap_start == 0:
                    return gap_start * MAX_COORD + pos_y, (gap_start, pos_y)


assert find_distress_signal(*ex1, 20, 20)[0] == 56000011

ANSWER = find_distress_signal(*inp)
print("Part 2 =", ANSWER)
assert ANSWER[0] == 11558423398893 # check with accepted answer
