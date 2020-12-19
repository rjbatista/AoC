import math

########
# PART 1

def get_asteroids(fn):
    asteroids = []
    with open("event2019/day10/" + fn, "r") as input:
        for y, row in enumerate(input):
            for x, col in enumerate(row):
                if (col == '#'):
                    asteroids.append((x, y))

    return asteroids


def calc_angle(a, b):
    ax, ay = a
    bx, by = b
    dx, dy = ax - bx, ay - by

    return math.atan2(dy, dx)


def count_detects(asteroids):
    visibility = {}
    for picked in asteroids:
        angles = set()
        for other in asteroids:
            if (other != picked):
                angles.add(calc_angle(picked, other))
        visibility[picked] = len(angles)

    return max(visibility.items(), key = lambda x: x[1])


assert (count_detects(get_asteroids("example1.txt"))) == ((3, 4), 8) # Best is 3,4 with 8 other asteroids detected
assert (count_detects(get_asteroids("example2.txt"))) == ((5, 8), 33) # Best is 5,8 with 33 other asteroids detected
assert (count_detects(get_asteroids("example3.txt"))) == ((1, 2), 35) # Best is 1,2 with 35 other asteroids detected
assert (count_detects(get_asteroids("example4.txt"))) == ((6, 3), 41) # Best is 6,3 with 41 other asteroids detected
assert (count_detects(get_asteroids("example5.txt"))) == ((11, 13), 210) # Best is 11,13 with 210 other asteroids detected

input_asteroids = get_asteroids("input.txt")
answer_p1 = count_detects(input_asteroids)
print("Part 1 =", answer_p1)
assert answer_p1 == ((29, 28), 256) # check with accepted answer

########
# PART 2

def calc_distance(a, b):
    ax, ay = a
    bx, by = b
    dx, dy = abs(ax - bx), abs(ay - by)

    return dx + dy

def rotate(a):
    return (a - (math.pi / 2)) % (2 * math.pi)

def get_asteroids_by_angle(station, asteroids):
    asteroids_by_angle = {}
    for other in asteroids:
        angle = calc_angle(station, other)

        if angle not in asteroids_by_angle:
            asteroids_by_angle[angle] = []

        asteroids_by_angle[angle] += [(calc_distance(station, other), other)]

    list = []
    for key, value in asteroids_by_angle.items():
        value.sort(key = lambda x : x[0], reverse = False)
        list += [(rotate(key), value)]

    list.sort()

    return list

def remove_n(asteroids_by_angle, count = 1):
    removed = None
    for _ in range(count):
        angle, list_by_dist = asteroids_by_angle.pop(0)

        removed = list_by_dist.pop(0)

        if (list_by_dist):
            asteroids_by_angle.append((angle, list_by_dist))

    return removed

# example p2
asteroids_by_angle = get_asteroids_by_angle((11, 13), get_asteroids("example5.txt"))
assert remove_n(asteroids_by_angle)[1] == (11, 12)      # The 1st asteroid to be vaporized is at 11,12.
assert remove_n(asteroids_by_angle)[1] == (12, 1)       # The 2nd asteroid to be vaporized is at 12,1.
assert remove_n(asteroids_by_angle)[1] == (12, 2)       # The 3rd asteroid to be vaporized is at 12,2.
assert remove_n(asteroids_by_angle, 7)[1] == (12, 8)    # The 10th asteroid to be vaporized is at 12,8.
assert remove_n(asteroids_by_angle, 10)[1] == (16, 0)   # The 20th asteroid to be vaporized is at 16,0.
assert remove_n(asteroids_by_angle, 30)[1] == (16, 9)   # The 50th asteroid to be vaporized is at 16,9.
assert remove_n(asteroids_by_angle, 50)[1] == (10, 16)  # The 100th asteroid to be vaporized is at 10,16.
assert remove_n(asteroids_by_angle, 99)[1] == (9, 6)    # The 199th asteroid to be vaporized is at 9,6.
assert remove_n(asteroids_by_angle, 1)[1] == (8, 2)     # The 200th asteroid to be vaporized is at 8,2.
assert remove_n(asteroids_by_angle, 1)[1] == (10, 9)    # The 201st asteroid to be vaporized is at 10,9.
assert remove_n(asteroids_by_angle, 99)[1] == (11, 1)   # The 299th and final asteroid to be vaporized is at 11,1.

asteroids_by_angle = get_asteroids_by_angle(answer_p1[0], input_asteroids)
answer_asteroid = remove_n(asteroids_by_angle, 200)[1]
answer = answer_asteroid[0] * 100 + answer_asteroid[1]
print("Part 2 =", answer_asteroid, answer)
assert answer == 1707 # check with accepted answer

