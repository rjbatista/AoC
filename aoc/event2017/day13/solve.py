from itertools import count
from collections import deque
import re

########
# PART 1

def read(filename):
    with open("event2017/day13/" + filename, "r") as file:
        pattern = re.compile(r"^(\d+): (\d+)$")

        firewall = {}
        for line in file:
            match = pattern.match(line)

            if match:
                firewall[int(match[1])] = int(match[2])
            else:
                raise RuntimeError("invalid input " + line)

        return firewall


def get_scanner_pos(layer_depth, t):
    s_pos = t % (layer_depth + layer_depth - 2)

    if s_pos >= layer_depth:
        s_pos = layer_depth - (s_pos - layer_depth) - 2

    return s_pos


def draw_firewall(firewall, t, delay = 0):
    print("Picosecond %d:" % t)
    total_layers = max(firewall.keys()) + 1
    max_depth = max(firewall.values())
    for n in range(total_layers):
        print("%3d " % n, end="")
    print()

    for depth in range(max_depth):
        for layer in range(total_layers):
            if layer in firewall:
                max_layer_depth = firewall[layer]

                if max_layer_depth > depth:
                    print(" [", end="")


                    if get_scanner_pos(max_layer_depth, t + delay) == depth:
                        print("S", end = "")
                    else:
                        print(" ", end = "")

                    print("]", end="")
                else:
                    print("    ", end="")
            else:
                if depth == 0:
                    print(" ...", end="")
                else:
                    print("    ", end="")
        print()


def calc_severity(firewall, starting_time = 0):
    total_layers = max(firewall.keys()) + 1

    total_cost = 0
    for depth in range(total_layers):
        if depth in firewall:
            layer_range = firewall[depth]
            if get_scanner_pos(layer_range, depth + starting_time) == 0:
                total_cost += depth * layer_range

    return total_cost


ex1_firewall = read("example1.txt")
assert calc_severity(ex1_firewall) == 24


firewall = read("input.txt")
answer = calc_severity(firewall)
print("Part 1 =", answer)
assert answer == 1624 # check with accepted answer


########
# PART 2

def calc_delay(firewall):
    for delay in count():
        valid = True
        for k, v in firewall.items():
            if get_scanner_pos(v, delay + k) == 0:
                valid = False
                break

        if valid:
            return delay


assert calc_delay(ex1_firewall) == 10

answer = calc_delay(firewall)
print("Part 2 =", answer)
assert answer == 3923436 # check with accepted answer
