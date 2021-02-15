from event2019.day09.computer_v3 import Computer_v3
from queue import Queue
from threading import Thread

########
# PART 1

computer = Computer_v3()

with open("event2019/day11/input.txt", "r") as input:
    code = [int(x) for x in input.readline().split(",")]

def get_painted_panels(original_value = 0):
    # setup the brain on a different thread
    computer = Computer_v3(code)
    computer.set_debug(False)
    input = Queue()
    output = Queue()
    t = Thread(target=computer.run, daemon=True, args=(input, output))
    t.start()

    # calculate
    _directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    panels = { (0,0): original_value }
    pos = (0, 0)
    current_direction = 0
    while t.is_alive():
        input.put(panels.get(pos, 0))
        color, turn_direction = output.get(), output.get()

        panels[(pos)] = color
        current_direction = (current_direction + (1 if turn_direction == 1 else -1)) % len(_directions)
        pos = tuple(map(sum, zip(pos, _directions[current_direction])))

    return panels

panels = get_painted_panels()
answer = len(panels.keys())
print("Part1 =", answer)
assert answer == 2511

########
# PART 2
def draw_panels(panels):
    bounds = (0, 0, 0, 0)
    for x, y in panels.keys():
        bounds = (min(bounds[0], x), min(bounds[1], y), max(bounds[2], x), max(bounds[3], y))

    min_x, min_y, max_x, max_y = bounds
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(' ' if panels.get((x, y), 0) == 0 else '#', end="")
        print()

panels = get_painted_panels(1)
draw_panels(panels)
print("Part2 = HJKJKGPH")
