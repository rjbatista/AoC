""" Advent of code 2017 - day 20 """
from pathlib import Path
from itertools import combinations
import re
import math

########
# PART 1

def read(filename):
    """ Read particles from file """
    particles = []

    particle_pattern = re.compile((r"^p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>,\s*"
        r"v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>,\s*"
        r"a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>$"))
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line_number, line in enumerate(file):
            match = particle_pattern.match(line)

            if match:
                values = list(map(int, match.groups()))
                pos = tuple(values[:3])
                vel = tuple(values[3:6])
                acc = tuple(values[6:])
                particles.append((line_number, pos, vel, acc))
            else:
                raise RuntimeError("Error on line " + str(line_number) + ": " + line)

    return particles


def manhattan(coord_x, coord_y, coord_z):
    """ calculate the manhattan distance """
    return abs(coord_x) + abs(coord_y) + abs(coord_z)


def get_position_at(time, particle):
    """ Calculate position at specified time """
    _, pos, vel, acc = particle
    p_x, p_y, p_z = pos
    v_x, v_y, v_z = vel
    a_x, a_y, a_z = acc

    p_x = p_x + (v_x + .5 * a_x) * time + .5 * a_x * time * time
    p_y = p_y + (v_y + .5 * a_y) * time + .5 * a_y * time * time
    p_z = p_z + (v_z + .5 * a_z) * time + .5 * a_z * time * time

    return p_x, p_y, p_z


def get_closest_particle_in_long_run(particles):
    """
    Get the closest particle in the long run.
    Simulate for a large t
    """

    time = 1e10 # just a large time
    distances = []
    for particle in particles:
        distances.append((manhattan(*get_position_at(time, particle)), particle[0]))

    return min(distances)

ex1 = read("example1.txt")
assert get_closest_particle_in_long_run(ex1)[1] == 0

inp = read("input.txt")
ANSWER = get_closest_particle_in_long_run(inp)[1]
print("Part 1 =", ANSWER)
assert ANSWER == 364 # check with accepted answer

########
# PART 2

def quadratic(coef_a, coef_b, coef_c):
    """ Solve the quadratic for ax^2 + bx + c """
    if coef_a == 0:
        if coef_b == 0:
            return [ 0.0 ] if coef_c == 0  else []

        return [-coef_c / coef_b]

    discriminant = coef_b**2 - 4 * coef_a * coef_c

    if discriminant < 0:
        return [] # only complex solutions - not relevant

    if discriminant == 0:
        return [-coef_b / 2 * coef_a]

    return [(-coef_b + math.sqrt(discriminant)) / (2 * coef_a),
        (-coef_b - math.sqrt(discriminant)) / (2 * coef_a)]


def solve_colision(particle1, particle2):
    """ find colisions between particles """
    _, (p1_x, _, _), (v1_x, _, _), (a1_x, _, _) = particle1
    _, (p2_x, _, _), (v2_x, _, _), (a2_x, _, _) = particle2

    colision_times = quadratic(.5 * (a1_x - a2_x),
        (v1_x + .5 * a1_x) - (v2_x + .5 * a2_x),
        p1_x - p2_x)

    colisions = []
    for time in colision_times:
        if time >= 0 and time.is_integer():
            pos1 = get_position_at(time, particle1)
            pos2 = get_position_at(time, particle2)

            # x matches, check the rest
            if pos1 == pos2:
                colisions.append(time)

    return colisions


def remove_colisions(particles):
    """ Find a remove all colisions """
    partset = set(particles)

    colisions = {}
    for particle1, particle2 in combinations(partset, 2):
        times = solve_colision(particle1, particle2)

        for time in times:
            colisions.setdefault(time, set()).update([particle1, particle2])

    for time, colision in sorted(colisions.items()):
        colision = [x for x in colision if x in partset]

        if len(colision) > 1:
            for particle in colision:
                partset.remove(particle)

    return partset


ex2 = read("example2.txt")
assert len(remove_colisions(ex2)) == 1

ANSWER = len(remove_colisions(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 420 # check with accepted answer
