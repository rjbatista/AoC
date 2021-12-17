import re

########
# PART 1

def read(filename):
    with open("event2021/day17/" + filename, "r") as file:
        match = re.match(r"^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$", file.readline().strip())

        if match:
            return ((int(match[1]), int(match[4])), (int(match[2]), int(match[3]))) # top left, bottom right
        else:
            raise RuntimeError()


def max_height(target):
    """
    Solved using this racionale:
        ignore x -- it's independent and can adapt to any value we specify for each starting y velocity (vy)
        with positive vy necessary for reaching height, vy will be -vy when y is 0 again
        so, the heighest initial velocity is reaching the minimum y target in one step, or vy = -min_y
        the height for this vy is vy + vy-1 + vy-2 + ... + vy-(vy-1) = sum(1..vy) = vy(vy - 1) / 2
    """
    min_y = -target[1][1]

    return min_y * (min_y - 1) // 2


ex1_target = read("example1.txt")
assert max_height(ex1_target) == 45

target = read("input.txt")
answer = max_height(target)
print("Part 1 =", answer)
assert answer == 4186 # check with accepted answer


########
# PART 2

def hits_target(target, vx, vy):
    (x1, y1), (x2, y2) = target

    x, y = 0, 0
    while True:
        x += vx
        y += vy

        vx -= 1 if vx > 0 else 0
        vy -= 1

        if x1 <= x <= x2 and y2 <= y <= y1:
            return True
        
        if x > x2 or y < y2:
            return False


def count_all(target):
    counter = 0
    for vx in range(target[1][0] + 1):
        for vy in range(target[1][1] - 1, -target[1][1]):
            if hits_target(target, vx, vy):
                counter += 1

    return counter


assert count_all(ex1_target) == 112

answer = count_all(target)
print("Part 2 =", answer)
assert answer == 2709 # check with accepted answer
