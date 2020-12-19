import numpy
import matplotlib.pyplot as plt

########
# PART 1
class WireMap:
    _INSTRUCTION_SET = {
        'L': (-1,  0),
        'R': ( 1,  0),
        'U': ( 0, -1),
        'D': ( 0,  1)
    }

    def __init__(self) -> None:
        self._points_by_id = {}
        self._x = 0
        self._y = 0
        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0
        self._collisions = set()

    def define_wire(self, id, input):
        self._x = 0
        self._y = 0
        for instruction in input.split(","):
            direction = self._INSTRUCTION_SET[instruction[0]]

            self.define_point(id, direction, int(instruction[1:]))

    def define_point(self, id, direction, length):
        self._x = self._x + direction[0] * length
        self._y = self._y + direction[1] * length
    
        self._points_by_id[id] = self._points_by_id.get(id, []) + [(self._x, self._y)]

        if (self._min_x > self._x): self._min_x = self._x
        if (self._max_x < self._x): self._max_x = self._x
        if (self._min_y > self._y): self._min_y = self._y
        if (self._max_y < self._y): self._max_y = self._y

    def calculate(self, draw = False):
        translate_x = -self._min_x if self._min_x < 0 else 0
        translate_y = -self._min_y if self._min_y < 0 else 0

        canvas = numpy.zeros((self._max_y + translate_y + 1, self._max_x + translate_x + 1))

        for id, points in self._points_by_id.items():
            x = 0
            y = 0
            for (px, py) in points:
                while (x != px or y != py):
                    current_value = canvas[y + translate_y][x + translate_x]

                    if (current_value > 0 and current_value != id and (x != 0 or y != 0)):
                        self._collisions.add((x,y))

                    canvas[y + translate_y][x + translate_x] += id
                    if (x < px): x += 1
                    if (x > px): x -= 1
                    if (y < py): y += 1
                    if (y > py): y -= 1
           
        if (draw):
            plt.imshow(canvas)
            plt.show()
    
    def get_collisions(self):
        return self._collisions

    def get_min_manhattan_distance(self):
        return min([abs(x) + abs(y) for x,y in wiremap._collisions])

    def get_wire_distance_to_point(self, point, points):
        dpx, dpy = point
        x = 0
        y = 0
        dist = 0
        for (px, py) in points:
            while (x != px or y != py):
                if (x == dpx and y == dpy):
                    return dist

                dist += 1
                if (x < px): x += 1
                if (x > px): x -= 1
                if (y < py): y += 1
                if (y > py): y -= 1

        return dist

    def get_min_wire_distance(self):
        min_dist = 9999999999
        for point in self._collisions:
            total_for_point = 0

            for _, wire in self._points_by_id.items():
                total_for_point += self.get_wire_distance_to_point(point, wire)

            min_dist = min(total_for_point, min_dist)

        return min_dist

    
# Example 1
wiremap = WireMap()
wiremap.define_wire(1, "R75,D30,R83,U83,L12,D49,R71,U7,L72")
wiremap.define_wire(2, "U62,R66,U55,R34,D71,R55,D58,R83")

wiremap.calculate()
assert wiremap.get_min_manhattan_distance() == 159

# Example 2
wiremap = WireMap()
wiremap.define_wire(1, "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
wiremap.define_wire(2, "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")

wiremap.calculate()
assert wiremap.get_min_manhattan_distance() == 135

# part 1
wiremap = WireMap()
id = 0
with open("event2019/day3/input.txt", "r") as input:
    for wire in input:
        id += 1
        wiremap.define_wire(id, wire)
wiremap.calculate()

answer = wiremap.get_min_manhattan_distance()
print("Part 1 =", answer)
assert answer == 1264 # check with accepted answer

########
# PART 2

# use already calculated from part 1
answer = wiremap.get_min_wire_distance()
print("Part 2 =", answer)
assert answer == 37390 # check with accepted answer

# Example 1
wiremap = WireMap()
wiremap.define_wire(1, "R75,D30,R83,U83,L12,D49,R71,U7,L72")
wiremap.define_wire(2, "U62,R66,U55,R34,D71,R55,D58,R83")
wiremap.calculate()

assert wiremap.get_min_wire_distance() == 610

# Example 2
wiremap = WireMap()
wiremap.define_wire(1, "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
wiremap.define_wire(2, "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
wiremap.calculate()

assert wiremap.get_min_wire_distance() == 410

