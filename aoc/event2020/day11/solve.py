########
# PART 1

def get_seating(fn):
    seats = {}
    width, height = 0, 0
    with open("event2020/day11/" + fn, "r") as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line[:-1]):
                seats[(x, y)] = ch
                width = x
            height = y

    return (width, height), seats


def print_seats(width, height, seats):
    for y in range(height + 1):
        for x in range(width + 1):
            print(seats[x, y], end = "")
        print()
    print()


def get_neighbours(seats, x, y):
    neighbours = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dx != 0 or dy != 0) and (x + dx, y + dy) in seats:
                neighbours.append(seats[(x + dx, y + dy)])

    return neighbours


def update_seats(seats, get_neighbours_func, min_occupied):
    to_occupy = []
    to_free = []
    for (x, y), ch in seats.items():
        neighbours = get_neighbours_func(seats, x, y)
        occupied_neighbours = sum([1 for ch in neighbours if ch == '#'])

        if ch == 'L': # empty
            if (occupied_neighbours == 0):
                to_occupy.append((x, y))
        elif ch == '#': # occupied
            if (occupied_neighbours >= min_occupied):
                to_free.append((x, y))

    for x, y in to_occupy:
        seats[(x, y)] = '#'

    for x, y in to_free:
        seats[(x, y)] = 'L'

    return to_occupy, to_free


def update_to_stable(dimension, seats, get_neighbours_func, min_occupied):
    rounds = 0
    while True:
        #print("round", rounds)
        #print_seats(*dimension, seats)
        rounds += 1
        to_occupy, to_free = update_seats(seats, get_neighbours_func, min_occupied)

        if not to_occupy and not to_free:
            break

    return rounds


def update_to_stable_p1(dimension, seats):
    return update_to_stable(dimension, seats, get_neighbours, 4)


dimension, seats = get_seating("example1.txt")
rounds = update_to_stable_p1(dimension, seats)
assert sum([1 for ch in seats.values() if ch == '#']) == 37

dimension, seats = get_seating("input.txt")
rounds = update_to_stable_p1(dimension, seats)
answer = sum([1 for ch in seats.values() if ch == '#'])
print("Part 1 =", answer)
assert answer == 2204 # check with accepted answer

########
# PART 2

def get_neighbours_p2(seats, x, y):
    neighbours = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dx != 0 or dy != 0):
                cx = x + dx
                cy = y + dy
                while (cx, cy) in seats:
                    seat = seats[(cx, cy)]
                    if seat != '.':
                        neighbours.append(seat)
                        break

                    cx = cx + dx
                    cy = cy + dy
    
    return neighbours


def update_to_stable_p2(dimension, seats):
    return update_to_stable(dimension, seats, get_neighbours_p2, 5)


dimension, seats = get_seating("example1.txt")
rounds = update_to_stable_p2(dimension, seats)
assert sum([1 for ch in seats.values() if ch == '#']) == 26

dimension, seats = get_seating("input.txt")
rounds = update_to_stable_p2(dimension, seats)
answer = sum([1 for ch in seats.values() if ch == '#'])
print("Part 2 =", answer)
assert answer == 1986 # check with accepted answer
