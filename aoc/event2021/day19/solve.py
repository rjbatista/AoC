from itertools import combinations
from dataclasses import dataclass, field
import re

########
# PART 1

# the 24 possible rotations of 90 degrees on all axis
ROTATION_FUNCTIONS = [
        lambda x, y, z: (x, y, z),
        lambda x, y, z: (y, z, x),
        lambda x, y, z: (z, x, y),
        lambda x, y, z: (-x, z, y),
        lambda x, y, z: (z, y, -x),
        lambda x, y, z: (y, -x, z),
        lambda x, y, z: (x, z, -y),
        lambda x, y, z: (z, -y, x),
        lambda x, y, z: (-y, x, z),
        lambda x, y, z: (x, -z, y),
        lambda x, y, z: (-z, y, x),
        lambda x, y, z: (y, x, -z),
        lambda x, y, z: (-x, -y, z),
        lambda x, y, z: (-y, z, -x),
        lambda x, y, z: (z, -x, -y),
        lambda x, y, z: (-x, y, -z),
        lambda x, y, z: (y, -z, -x),
        lambda x, y, z: (-z, -x, y),
        lambda x, y, z: (x, -y, -z),
        lambda x, y, z: (-y, -z, x),
        lambda x, y, z: (-z, x, -y),
        lambda x, y, z: (-x, -z, -y),
        lambda x, y, z: (-z, -y, -x),
        lambda x, y, z: (-y, -x, -z)
]


def read(filename):
    with open("event2021/day19/" + filename, "r") as file:
        scanner_pattern = re.compile(r"^--- scanner (\d+) ---$")
        beacon_pattern = re.compile(r"^(-?\d+),(-?\d+),(-?\d+)$")

        scanner_data = {}

        line = file.readline().strip()
        while line:
            match = scanner_pattern.match(line)
            if match:
                scanner = int(match[1])

                beacons = []

                line = file.readline().strip()
                while line != '':
                    match = beacon_pattern.match(line)

                    if match:
                        beacons += [Beacon(int(match[1]), int(match[2]), int(match[3]))]
                        line = file.readline().strip()
                    else:
                        raise RuntimeError("invalid input " + line)

                scanner_data[scanner] = beacons

                # gather its relatives
                for beacon in beacons:
                    beacon.calculate_relatives(beacons)

                assert len(beacons) < 30

                line = file.readline().strip()
            else:
                raise RuntimeError("invalid input " + line)

        return scanner_data


@dataclass(frozen=True)
class Beacon():
    x: int
    y: int
    z: int
    _relatives: set = field(default_factory=set, init=False, repr=False, hash=False, compare=False)


    def calculate_relatives(self, beacon_list):
        self._relatives.clear()

        for beacon in beacon_list:
            self._relatives.add((beacon.x - self.x, beacon.y - self.y, beacon.z - self.z))

        pass


    def __lt__(self, other) -> bool:
        return self.x < other.x if self.x != other.x else self.y < other.y if self.y != other.y else self.z < other.z


# need to think this over to optimize the process when I have time
def map_beacons(scanner_data : dict):
    known_scanners = set([(0, 0, 0)])
    total = len(scanner_data)

    # assume scanner 0 orientation, so consider it's beacons as being in the normalized positions
    known_beacons = set(scanner_data.pop(0))

    while scanner_data:
        matches = False
        for scanner, unknown_beacons in scanner_data.items():
            print(int((len(scanner_data) / total) * 100), "%", end="\r")
            for unknown in unknown_beacons:
                for rotation_function in ROTATION_FUNCTIONS:
                    relatives = { rotation_function(*p) for p in unknown._relatives }

                    for known in known_beacons:
                        if len(relatives.intersection(known._relatives)) >= 12:
                            matches = True
                            nx, ny, nz = rotation_function(unknown.x, unknown.y, unknown.z)
                            dx, dy, dz = nx - known.x, ny - known.y, nz - known.z

                            known_scanners.add((dx, dy, dz))
                            scanner_data.pop(scanner)

                            for new_beacon in unknown_beacons:
                                x, y, z = rotation_function(new_beacon.x, new_beacon.y, new_beacon.z)
                                x, y, z = x - dx, y - dy, z - dz

                                known_beacons.add(Beacon(x, y, z))

                            break

                if matches:
                    break

            if matches:
                break

        if matches:
            for beacon in known_beacons:
                beacon.calculate_relatives(known_beacons)

    return known_beacons, known_scanners


ex_beacons, ex_scanners = map_beacons(read("example1.txt"))
assert len(ex_beacons) == 79

#import cProfile
#cProfile.run("beacons, scanners = map_beacons(read('input.txt'))")

beacons, scanners = map_beacons(read("input.txt"))
answer = len(beacons)
print("Part 1 =", answer)
assert answer == 467 # check with accepted answer

########
# PART 2

def find_largest_distance(scanners):
    max_distance = 0

    for ((x1, y1, z1), (x2, y2, z2)) in combinations(scanners, 2):
        max_distance = max(max_distance, abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1))
    
    return max_distance


assert find_largest_distance(ex_scanners) == 3621

answer = find_largest_distance(scanners)
print("Part 2 =", answer)
assert answer == 12226 # check with accepted answer

