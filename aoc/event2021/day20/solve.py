########
# PART 1


def read(filename):
    with open("event2021/day20/" + filename, "r") as file:
        key = 0
        for bit in reversed(file.readline().strip()):
            key = (key << 1) + (1 if bit == '#' else 0)

        file.readline()

        image = {}
        for y, line in enumerate(file):
            for x, ch in enumerate(line.strip()):
                image[(x, y)] = (1 if ch == '#' else 0)
                

        return (image, 0), key


def image_enhancement_algorithm(image, key):
    image_data, infinity_value = image
    new_image_data = {}

    todo = set(image_data.keys())
    min_x, max_x = 0, 0
    min_y, max_y = 0, 0
    for x, y in image_data.keys():
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

    min_x, min_y = min_x - 1, min_y - 1
    max_x, max_y = max_x + 1, max_y + 1

    while todo:
        (x, y) = todo.pop()
        
        if (x, y) not in new_image_data:
            lookup = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    lookup = (lookup << 1) + image_data.get((x + dx, y + dy), infinity_value)

            value = (key >> lookup) & 1
            new_image_data[(x, y)] = value

            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if min_x <= nx <= max_x and min_y <= ny <= max_y and (nx, ny) not in new_image_data:
                        todo.add((x + dx, y + dy))

    return new_image_data, (key & 1) ^ infinity_value


def draw_image(image):
    image_data, infinity_value = image

    min_x, max_x = 0, 0
    min_y, max_y = 0, 0

    for x, y in image_data.keys():
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
    
    min_x, min_y = min_x - 5, min_y - 5
    max_x, max_y = max_x + 5, max_y + 5

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if image_data.get((x, y), infinity_value) == 1 else '.', end="")
        print()
    print()


ex_image, ex_key = read("example1.txt")
ex_image = image_enhancement_algorithm(ex_image, ex_key)
ex_image = image_enhancement_algorithm(ex_image, ex_key)
assert sum(ex_image[0].values()) == 35


image, key = read("input.txt")
image = image_enhancement_algorithm(image, key)
image = image_enhancement_algorithm(image, key)
answer = sum(image[0].values())
print("Part 1 =", answer)
assert answer == 5498 # check with accepted answer

########
# PART 2

for _ in range(50 - 2):
    ex_image = image_enhancement_algorithm(ex_image, ex_key)

assert sum(ex_image[0].values()) == 3351

for _ in range(50 - 2):
    image = image_enhancement_algorithm(image, key)


answer = sum(image[0].values())
print("Part 2 =", answer)
assert answer == 16014 # check with accepted answer
