import heapq

########
# PART 1

def read(filename):
    with open("event2021/day15/" + filename, "r") as file:
        return [[int(ch) for ch in line.strip()] for line in file.readlines()]
    

def find_best_path(cave):
    width, height = len(cave[0]), len(cave)
    todo = [(0, 0, 0)]
    heapq.heapify(todo);

    already_visited = { (0,0): 0 }
    while todo:
        cost, x, y = heapq.heappop(todo)

        if (x, y) == (width - 1, height - 1):
            return cost

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height:
                new_cost = cost + cave[ny][nx]

                if (nx, ny) in already_visited:
                    best_cost = already_visited[(nx, ny)]

                    to_add = new_cost < best_cost
                else:
                    to_add = True

                if to_add:
                    heapq.heappush(todo, (new_cost, nx, ny))
                    already_visited[(nx, ny)] = new_cost


ex1_cave = read("example1.txt")
assert find_best_path(ex1_cave) == 40


cave = read("input.txt")
answer = find_best_path(cave)
print("Part 1 =", answer)
assert answer == 824 # check with accepted answer

########
# PART 2

def five_times_cave(cave):
    width, height = len(cave[0]), len(cave)
    new_cave = []
    for y in range(height * 5):
        row = []
        for x in range(width * 5):
            v = cave[y % height][x % width]

            v += int(x / width) + int(y / height)

            if v > 9:
                v -= 9

            row.append(v)
        new_cave.append(row)

    return new_cave


def draw_cave(cave):
    for row in cave:
        for col in row:
            print(col, end="")
        print()
    print()


ex1_cave_p2 = five_times_cave(ex1_cave)
assert find_best_path(ex1_cave_p2) == 315


cave_p2 = five_times_cave(cave)
answer = find_best_path(cave_p2)
print("Part 2 =", answer)
assert answer == 3063 # check with accepted answer
