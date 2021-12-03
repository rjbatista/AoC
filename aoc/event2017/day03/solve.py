########
# PART 1

# Wiki for Ulam spiral
# https://en.wikipedia.org/wiki/Ulam_spiral


def calc_spiral_position(inp):
    # search the diagonal
    n = 0
    while (4 * pow(n, 2) - 2 * n + 1 <= inp):
        n += 1

    n -= 1
    
    # so, it's in this line, just have to figure out here by the difference
    diff = inp - (4 * pow(n, 2) - 2 * n + 1)
    if diff <= 2 * n:
        return n - diff, n
    elif diff <= 4 * n:
        return -n, n - diff + 2 * n
    elif diff <= 6 * n:
        return - n + diff - 4 * n, -n
    else:
        return n + 1, -n + diff - 6 * n - 1


# Data from square 1 is carried 0 steps, since it's at the access port.
assert sum(map(abs, calc_spiral_position(1))) == 0
# Data from square 12 is carried 3 steps, such as: down, left, left.
assert sum(map(abs, calc_spiral_position(12))) == 3
# Data from square 23 is carried only 2 steps: up twice.
assert sum(map(abs, calc_spiral_position(23))) == 2
# Data from square 1024 must be carried 31 steps.
assert sum(map(abs, calc_spiral_position(1024))) == 31

inp = 325489
answer = sum(map(abs, calc_spiral_position(inp)))
print("Part 1 =", answer)
assert answer == 552 # check with accepted answer


########
# PART 2

# guess I'll really build the spiral that I avoided on part 1...
def gen_spiral():
    x, y = 0, 0
    dx, dy = 1, 0
    yield x, y
    
    radius = 0
    while (True):
        for _ in range(2):
            for _ in range(radius + 1):
                x += dx
                y -= dy
                yield x, y
            dx, dy = -dy, dx # turn

        radius += 1


def calc_value_for_pos(square, coords, _):
    val = 0

    x, y = coords

    if (x, y) == (0, 0):
        return 1

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if ((x != 0 or y != 0) and (x + dx, y + dy) in square):
                val += square[(x + dx, y + dy)]
    
    return val


def build_square(max, print_square = False):
    square = {}

    g = gen_spiral()
    i = 0
    while (True):
        x, y = next(g)
        i += 1
        val = calc_value_for_pos(square, (x, y), i)
        square[x, y] = val
        if (val > max):
            break

    max_coords = x, y

    if (print_square):
        for y in range(-5, 5):
            for x in range(-5, 5):
                    print(square[x, y] if (x, y) in square else "-", end="\t")
            print()

    return max_coords, val


# uncomment to see the square
# build_square(inp, True)

answer = build_square(inp)[1]
print("Part 2 =", answer)
assert answer == 330785 # check with accepted answer
