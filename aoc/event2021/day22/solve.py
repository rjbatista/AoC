from dataclasses import dataclass
import re

########
# PART 1

@dataclass
class Cuboid:
    state: bool
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def outside_region(self, region_size = 50):
        return any([True for v in [self.x1, self.y1, self.z1, self.x2, self.y2, self.z2] if abs(v) > region_size])


    def volume(self):
        volume = (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

        assert self.x2 >= self.x1
        assert self.y2 >= self.y1
        assert self.z2 >= self.z1

        return volume if self.state else -volume


    def intersect(self, other: 'Cuboid') -> 'Cuboid':
        if self.x2 < other.x1 or self.x1 > other.x2:
            return None
        if self.y2 < other.y1 or self.y1 > other.y2:
            return None
        if self.z2 < other.z1 or self.z1 > other.z2:
            return None

        return Cuboid(other.state if self.state != other.state else not other.state,
            max(self.x1, other.x1),
            max(self.y1, other.y1),
            max(self.z1, other.z1),
            min(self.x2, other.x2),
            min(self.y2, other.y2),
            min(self.z2, other.z2))


def read(filename):
    with open("event2021/day22/" + filename, "r") as file:
        pattern = re.compile(r"^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$")
        cuboids = []

        for line in file:
            match = pattern.match(line)
            if match:
                x1, x2 = sorted((int(match[2]), int(match[3])))
                y1, y2 = sorted((int(match[4]), int(match[5])))
                z1, z2 = sorted((int(match[6]), int(match[7])))
                cuboids.append(Cuboid(match[1] == "on", x1, y1, z1, x2, y2, z2))
            else:
                raise RuntimeError("invalid input " + line)

        return cuboids


def curate_cuboids(cuboids, include_outside = False):
    curated_cuboids = []
    for cuboid in cuboids:
        if include_outside or not cuboid.outside_region():
            for curated_cuboid in curated_cuboids[:]:
                new_cuboid = curated_cuboid.intersect(cuboid)

                if new_cuboid:
                    curated_cuboids.append(new_cuboid)

            if cuboid.state:
                curated_cuboids.append(cuboid)

    return curated_cuboids


ex1 = read("example1.txt")
assert sum([c.volume() for c in curate_cuboids(ex1)]) == 39

ex2 = read("example2.txt")
assert sum(c.volume() for c in curate_cuboids(ex2)) == 590784

inp = read("input.txt")
answer = sum(c.volume() for c in curate_cuboids(inp))
print("Part 1 =", answer)
assert answer == 603661 # check with accepted answer

########
# PART 2

ex3 = read("example3.txt")
assert sum(c.volume() for c in curate_cuboids(ex3, True)) == 2758514936282235

answer = sum(c.volume() for c in curate_cuboids(inp, True))
print("Part 2 =", answer)
assert answer == 1237264238382479 # check with accepted answer
