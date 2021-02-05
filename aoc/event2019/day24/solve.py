########
# PART 1

def get_initial_state(fn):
    state = {}
    with open("event2019/day24/" + fn, "r") as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line[:-1]):
                state[(x, y, 0)] = (ch == '#')

    return state


def do_cycle(current_state):
    new_state = {}
    for (x, y, z), bug in current_state.items():
        active_neighbours = 0
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nx, ny = x + dx, y + dy

            if current_state.get((nx, ny, z), False):
                active_neighbours += 1

        new_state[(x, y, z)] = (not bug and (1 <= active_neighbours <= 2)) or (bug and active_neighbours == 1)

    return new_state


def print_state(current_state):
    for y in range(5):
        for x in range(5):
            print('#' if current_state[x, y, 0] else '.', end="")
        print()

    print()


def calc_biodiversity_rating(state):
    total = 0
    for y in range(5):
        for x in range(5):
            if state[(x, y, 0)]:
                total += 1 << (y * 5 + x)
    
    return total


def run_till_match(state):
    visited = set()
    while True:
        bio = calc_biodiversity_rating(state)

        if bio in visited:
            break

        visited.add(bio)

        state = do_cycle(state)
    
    return state, bio


state = get_initial_state("example1.txt")
assert run_till_match(state)[1] == 2129920

answer = run_till_match(get_initial_state("input.txt"))[1]
print("Part 1 =", answer)
assert answer == 19923473 # check with accepted answer

########
# PART 2
def print_state_p2(current_state):
    min_z, max_z = 1000, -1000

    for (_, _, z), bug in current_state.items():
        if bug:
            min_z = min(min_z, z)
            max_z = max(max_z, z)

    for z in range(min_z, max_z + 1):
        print(f"Depth {z}:")
        for y in range(5):
            for x in range(5):
                if x == 2 and y == 2:
                    print("?", end = "")
                else:
                    print('#' if current_state.get((x, y, z), False) else '.', end="")
            print()

    print()


def do_cycle_p2(current_state):
    to_process = [state for state in current_state.keys()]
    accounted = set(to_process)
    new_state = {}
    while to_process:
        x, y, z = to_process.pop()

        active_neighbours = 0
        neighbours = [(x + dx, y + dy, z) for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]]
        for nx, ny, nz in neighbours:
            if 0 <= nx < 5 and 0 <= ny < 5:
                if nx == 2 and ny == 2:
                    dx, dy = nx - x, ny - y
                    if dx < 0:
                        neighbours += [(4, y, nz + 1) for y in range(5)]
                    elif dx > 0:
                        neighbours += [(0, y, nz + 1) for y in range(5)]
                    elif dy < 0:
                        neighbours += [(x, 4, nz + 1) for x in range(5)]
                    elif dy > 0:
                        neighbours += [(x, 0, nz + 1) for x in range(5)]

                    continue
                else:
                    if current_state.get((nx, ny, nz), False):
                        active_neighbours += 1
            else:
                if nx < 0:
                    neighbours += [(1, 2, nz - 1)]
                elif nx >= 5:
                    neighbours += [(3, 2, nz - 1)]
                elif ny < 0:
                    neighbours += [(2, 1, nz - 1)]
                elif ny >= 5:
                    neighbours += [(2, 3, nz - 1)]

                continue

            if (nx, ny) == (2, 2):
                print("WTF!")

            if (x, y, z) in current_state and (nx, ny, nz) not in accounted:
                to_process.append((nx, ny, nz))
                accounted.add((nx, ny, nz))

        bug = current_state.get((x, y, z), False)
        new_state[(x, y, z)] = (not bug and (1 <= active_neighbours <= 2)) or (bug and active_neighbours == 1)

    return new_state


def count_bugs(state):
    return sum([1 for _, bug in state.items() if bug])


state = get_initial_state("example1.txt")
for _ in range(10):
    state = do_cycle_p2(state)

assert count_bugs(state) == 99


state = get_initial_state("input.txt")
# remove the middle on the base floor
state.pop((2, 2, 0))

for _ in range(200):
    state = do_cycle_p2(state)

answer = count_bugs(state)
print("Part 2 =", answer)
assert answer == 1902 # check with accepted answer
