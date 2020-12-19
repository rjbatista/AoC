
########
# PART 1

def get_initial_state(fn):
    cubes = {}
    with open("event2020/day17/" + fn, "r") as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line[:-1]):
                if ch == '#':
                    cubes[(x, y, 0)] = True

    return cubes


def do_cycle(current_state):
    to_process = [cube for cube in current_state.keys()]
    accounted = set(to_process)
    new_state = {}
    while to_process:
        x, y, z = to_process.pop()

        active_neighbours = 0
        for dz in range(-1, 2, 1):
            for dy in range(-1, 2, 1):
                for dx in range(-1, 2, 1):
                    if dx != 0 or dy != 0 or dz != 0:
                        nx, ny, nz = x + dx, y + dy, z + dz

                        if current_state.get((nx, ny, nz), False):
                            active_neighbours += 1

                        if (x, y, z) in current_state and (nx, ny, nz) not in accounted:
                            to_process.append((nx, ny, nz))
                            accounted.add((nx, ny, nz))

        if current_state.get((x, y, z), False):
            # is active
            if 2 <= active_neighbours <= 3:
                new_state[(x, y, z)] = True
        else:
            if active_neighbours == 3:
                new_state[(x, y, z)] = True

    return new_state


def print_state(current_state):
    min_x, max_x = 1000, 0
    min_y, max_y = 1000, 0
    min_z, max_z = 1000, 0

    for (x, y, z), v in current_state.items():
        if v:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)
    
    for z in range(min_z, max_z + 1):
        print("z =", z)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print('#' if current_state.get((x, y, z), False) else '.', end="")
            print()
    print()
        

current_state = get_initial_state("example1.txt")
for _ in range(6):
    current_state = do_cycle(current_state)
assert sum([1 for state in current_state.values() if state]) == 112


current_state = get_initial_state("input.txt")
for _ in range(6):
    current_state = do_cycle(current_state)
answer = sum([1 for state in current_state.values() if state])
print("Part 1 =", answer)
assert answer == 265

########
# PART 2

def get_initial_state_p2(fn):
    cubes = {}
    with open("event2020/day17/" + fn, "r") as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line[:-1]):
                if ch == '#':
                    cubes[(x, y, 0, 0)] = True

    return cubes


def do_cycle_p2(current_state):
    to_process = [cube for cube in current_state.keys()]
    accounted = set(to_process)
    new_state = {}
    while to_process:
        x, y, z, w = to_process.pop()

        active_neighbours = 0
        for dw in range(-1, 2, 1):
            for dz in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    for dx in range(-1, 2, 1):
                        if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                            nx, ny, nz, nw = x + dx, y + dy, z + dz, w + dw

                            if current_state.get((nx, ny, nz, nw), False):
                                active_neighbours += 1

                            if (x, y, z, w) in current_state and (nx, ny, nz, nw) not in accounted:
                                to_process.append((nx, ny, nz, nw))
                                accounted.add((nx, ny, nz, nw))

        if current_state.get((x, y, z, w), False):
            # is active
            if 2 <= active_neighbours <= 3:
                new_state[(x, y, z, w)] = True
        else:
            if active_neighbours == 3:
                new_state[(x, y, z, w)] = True

    return new_state


def print_state_p2(current_state):
    min_x, max_x = 1000, 0
    min_y, max_y = 1000, 0
    min_z, max_z = 1000, 0
    min_w, max_w = 1000, 0

    for (x, y, z, w), v in current_state.items():
        if v:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)
            min_w = min(min_w, w)
            max_w = max(max_w, w)

    for w in range(min_w, max_w + 1):
        for z in range(min_z, max_z + 1):
            print("z =", z, ", w = ", w)
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    print('#' if current_state.get((x, y, z, w), False) else '.', end="")
                print()
    print()


#current_state = get_initial_state_p2("example1.txt")
#for _ in range(6):
#    current_state = do_cycle_p2(current_state)
#assert sum([1 for state in current_state.values() if state]) == 848


current_state = get_initial_state_p2("input.txt")
for _ in range(6):
    current_state = do_cycle_p2(current_state)
answer = sum([1 for state in current_state.values() if state])
print("Part 1 =", answer)
assert answer == 1936
