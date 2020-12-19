import re
from functools import reduce
from itertools import combinations
from math import gcd

########
# PART 1
def get_moons(fn):
    ret = []
    with open("event2019/day12/" + fn, "r") as input:
        pattern = re.compile(r"^<\w=(-?\d+), \w=(-?\d+), \w=(-?\d+)>$")
        for line in input:
            m = re.match(pattern, line)
            if m:
                ret.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    
    return ret

def print_moons(moons):
    for (x, y, z), (vx, vy, vz) in moons:
        print(f"pos=<x={x:>3}, y={y:>3}, z={z:>3}>, vel=<x={vx:>3}, y={vy:>3}, z={vz:>3}>")

# gravity
def gravity(ca, cb):
    return -1 if ca > cb else 1 if ca < cb else 0

def step(moons):
    # apply gravity
    for ia, ib in combinations(range(len(moons)), 2):
        ((xa, ya, za), (vxa, vya, vza)) = moons[ia]
        ((xb, yb, zb), (vxb, vyb, vzb)) = moons[ib]

        gx, gy, gz = gravity(xa, xb), gravity(ya, yb), gravity(za, zb)

        moons[ia] = (xa, ya, za), (vxa + gx, vya + gy, vza + gz)
        moons[ib] = (xb, yb, zb), (vxb - gx, vyb - gy, vzb - gz)

    # apply velocity
    for i, m in enumerate(moons):
        (x, y, z), (vx, vy, vz) = m
        moons[i] = (x + vx, y + vy, z + vz), (vx, vy, vz)


moons = [((x, y, z), (0, 0, 0)) for x,y,z in get_moons("example1.txt")]
for _ in range(10): step(moons)
assert moons == [((2, 1, -3), (-3, -2, 1)), ((1, -8, 0), (-1, 1, 3)), ((3, -6, 1), (3, 2, -3)), ((2, 0, 4), (1, -1, -1))]
assert sum([(abs(x) + abs(y) + abs(z)) * (abs(vx) + abs(vy) + abs(vz)) for (x,y,z),(vx,vy,vz) in moons]) == 179

moons = [((x, y, z), (0, 0, 0)) for x,y,z in get_moons("input.txt")]
for _ in range(1000): step(moons)
answer = sum([(abs(x) + abs(y) + abs(z)) * (abs(vx) + abs(vy) + abs(vz)) for (x,y,z),(vx,vy,vz) in moons])
print("Part 1 =", answer)
assert answer == 13500

########
# PART 2
def lcm(values):
    ''' least common multiple '''
    return reduce(lambda a, b: a * b // gcd(a, b), values)

def get_periods(moons):
    orig_moons = moons[:]
    step(moons)

    periods = [None, None, None]
    p = 1
    while not periods[0] or not  periods[1] or not  periods[2]:
        step(moons)
        p += 1

        for axis in range(3):
            if not periods[axis]:
                found = True
                for moon_index in range(len(moons)):
                    if moons[moon_index][0][axis] != orig_moons[moon_index][0][axis] or moons[moon_index][1][axis] != orig_moons[moon_index][1][axis]:
                        found = False
                        break

                if found:
                    periods[axis] = p

    return periods

assert (lcm(get_periods([((x, y, z), (0, 0, 0)) for x,y,z in get_moons("example1.txt")]))) == 2772
assert (lcm(get_periods([((x, y, z), (0, 0, 0)) for x,y,z in get_moons("example2.txt")]))) == 4686774924

answer = lcm(get_periods(moons))
print("Part 2 =", answer)
assert answer == 278013787106916 # check with accepted answer
