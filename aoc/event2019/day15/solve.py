from event2019.day13.computer_v4 import Computer_v4
from queue import Queue
from threading import Thread
from time import sleep

########
# PART 1

with open("event2019/day15/input.txt", "r") as file:
    code = [int(x) for x in file.readline().split(",")]

# setup the brain on a different thread
computer = Computer_v4(code)
computer_in = Queue()
computer_out = Queue()
t = Thread(target=computer.run, daemon=True, args=(computer_in, computer_out))
t.start()

def get_new_position(pos, command):
    return {
        1: lambda x, y: (x, y - 1),
        2: lambda x, y: (x, y + 1),
        3: lambda x, y: (x - 1, y),
        4: lambda x, y: (x + 1, y)
    }[command](*pos)


def print_area(area, path = None):
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for x, y in area.keys():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (path and (x, y) in path):
                print(end="\033[91m")
            print(end=area.get((x, y), ' '))
            print(end="\033[0m")

        print()


def get_return_command(command):
    return {
        1: 2,
        2: 1,
        3: 4,
        4: 3,
    }[command]


area = {(0,0): '.'}
available_commands = [1, 2, 3, 4]
path = []
pos = (0, 0)
dest = None
visited = {pos}
best_path = None
while available_commands:

    command = available_commands.pop()
    computer_in.put(command)
    new_pos = get_new_position(pos, command)
    status = computer_out.get()
    if status == 0:
        area[new_pos] = '#'
    elif status == 1 or status == 2:
        if (new_pos not in visited):
            area[new_pos] = '.'
            path += [pos]
            visited.add(pos)
            return_command = get_return_command(command)
            available_commands.append(return_command)
            available_commands += [x for x in [1, 2, 3, 4] if x != return_command]
        else:
            path.pop()

        if status == 2:
            area[new_pos] = 'E'
            dest = new_pos
            if (best_path == None or len(path) < best_path):
                best_path = path[:]

        pos = new_pos


    pass

print_area(area, best_path)

answer = len(best_path)
print("Part 1 =", answer)
assert answer == 354 # check with accepted answer

########
# PART 2

to_visit = [(0, dest)]
visited = set()
count = 0
max_dist = 0
while to_visit:
    dist, pos = to_visit.pop(0)
    visited.add(pos)
    max_dist = max(max_dist, dist)

    for i in range(1, 5):
        possible_pos = get_new_position(pos, i)
        if (area[possible_pos] == '.'):
            if possible_pos not in visited:
                to_visit.append((dist + 1, possible_pos))

print("Part 2 =", max_dist)
assert max_dist == 370 # check with accepted answer
