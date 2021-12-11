########
# PART 1

class Colors:
    FLASHED = '\033[1m'
    RESET = '\033[0m'


def read(filename):
    with open("event2021/day11/" + filename, "r") as file:
        return [[int(ch) for ch in line.strip()] for line in file]


def step(octopuses):
    flash = []
    flashed = set()
    width, height = len(octopuses[0]), len(octopuses)

    for y, row in enumerate(octopuses):
        for x in range(width):
            row[x] += 1

            if row[x] > 9:
                flash.append((x, y))

    while flash:
        (x, y) = flash.pop()

        if (x, y) not in flashed:
            flashed.add((x, y))

            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 or dy != 0:
                        nx, ny = x + dx, y + dy

                        if 0 <= nx < width and 0 <= ny < height:
                            octopuses[ny][nx] += 1
                            
                            if octopuses[ny][nx] > 9 and (nx, ny) not in flashed:
                                flash.append((nx, ny))
    
    for y, row in enumerate(octopuses):
        for x in range(width):
            row[x] = row[x] if row[x] <= 9 else 0


def draw_octopuses(octopuses):
    for row in octopuses:
        for octopus in row:
            if octopus == 0:
                print(Colors.FLASHED, end="")
            print(str(octopus) + Colors.RESET, end="")
        print()
    print()


def count_flashes(octopuses, rounds, print_octopuses = False):
    total_flashes = 0
    for n in range(100):
        if print_octopuses:
            print("After step", n + 1)

        step(octopuses)
        total_flashes += sum([1 for row in octopuses for octopus in row if octopus == 0])

        if print_octopuses:
            draw_octopuses(ex1)
    
    return total_flashes


ex1 = read("example1.txt")
assert count_flashes(ex1, 100) == 1656


octopuses = read("input.txt")
answer = count_flashes(octopuses, 100)
print("Part 1 =", answer)
assert answer == 1591 # check with accepted answer


########
# PART 2

def find_total_flash(octopuses, print_octopuses = False):
    n  = 0
    while True:
        n += 1
        if print_octopuses:
            print("After step", n + 1)

        step(octopuses)
        unflashed = sum([1 for row in octopuses for octopus in row if octopus != 0])
        if unflashed == 0:
            return n

        if print_octopuses:
            draw_octopuses(ex1)


ex1 = read("example1.txt")
assert find_total_flash(ex1) == 195


octopuses = read("input.txt")
answer = find_total_flash(octopuses)
print("Part 2 =", answer)
assert answer == 314 # check with accepted answer
