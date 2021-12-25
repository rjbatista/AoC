
########
# PART 1

def read(filename):
    with open("event2021/day25/" + filename, "r") as file:
        rows = [line.strip() for line in file.readlines()]
        return [ch for row in rows for ch in row], len(rows[0]), len(rows)


def draw(region_data):
    region, width, height = region_data
    for y in range(height):
        for x in range(width):
            print(region[(y * width) + x], end="")
        print()
    print()


def find_standstill(region_data, debug = False, should_draw = None, max_steps = -1):
    region, width, height = region_data
    steps = 0
    while True:
        if debug:
            print("step", steps)
            if should_draw and should_draw(steps):
                draw((region, width, height))
            
            if steps == max_steps:
                return None

        stepped = False
        new_region = region[:]
        for y in range(height):
            for x in range(width):
                ch = region[(y * width) + x]
                if ch == '>':
                    if region[(y * width) + ((x + 1) % width)] == '.':
                        new_region[(y * width) + x] = '.'
                        new_region[(y * width) + ((x + 1) % width)] = '>'
                        stepped = True

        region = new_region
        new_region = region[:]
        for y in range(height):
            for x in range(width):
                ch = region[(y * width) + x]
                if ch == 'v':
                    if region[((y + 1) % height) * width + x] == '.':
                        new_region[(y * width) + x] = '.'
                        new_region[((y + 1) % height) * width + x] = 'v'
                        stepped = True

        steps += 1

        if not stepped:
            break

        region = new_region
    
    return steps
        



#ex1 = read("example1.txt")
#find_standstill(ex1, True, lambda _: True, max_steps=4)


ex2 = read("example2.txt")
assert find_standstill(ex2, True, lambda x: x in [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 55, 56, 57, 58, 59], 60) == 58


inp = read("input.txt")
answer = find_standstill(inp)
print("Part 1 =", answer)
assert answer == 456 # check with accepted answer
