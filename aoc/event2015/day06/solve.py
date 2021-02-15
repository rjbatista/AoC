import re

########
# PART 1

class Lights:
    def __init__(self, size):
        self.lights = [[0 for _ in range(size)] for _ in range(size)]


    def turn_on(self, start, end):
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                self.lights[y][x] = 1


    def turn_off(self, start, end):
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                self.lights[y][x] = 0


    def toggle(self, start, end):
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                self.lights[y][x] = not self.lights[y][x]


    def count_lights(self):
        return sum([column for row in self.lights for column in row if column])


def calc(lights):
    with open('event2015/day06/input.txt') as f:
        pattern = re.compile(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")
        for line in f:
            m = pattern.match(line)

            action = m.group(1)
            start = (int(m.group(2)), int(m.group(3)))
            end = (int(m.group(4)), int(m.group(5)))

            if (action == 'turn on'): lights.turn_on(start, end)
            if (action == 'turn off'): lights.turn_off(start, end)
            if (action == 'toggle'): lights.toggle(start, end)

    return lights.count_lights()


answer = calc(Lights(1000))
print("Part 1 =", answer)
assert answer == 543903 # check with accepted answer

########
# PART 2

class NewLights(Lights):
    def __init__(self, size):
        self.lights = [[0 for _ in range(size)] for _ in range(size)]


    def turn_on(self, start, end):
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                self.lights[y][x] += 1


    def turn_off(self, start, end):
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                self.lights[y][x] = max(self.lights[y][x] - 1, 0)


    def toggle(self, start, end):
        for y in range(start[1], end[1] + 1):
            for x in range(start[0], end[0] + 1):
                self.lights[y][x] += 2


answer = calc(NewLights(1000))
print("Part 2 =", answer)
assert answer == 14687245 # check with accepted answer
