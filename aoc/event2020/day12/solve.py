from math import sin, cos, radians

########
# PART 1

def get_commands(fn):
    with open("event2020/day12/" + fn) as file:
        for line in file:
            yield line[:1], int(line[1:])


def get_final_pos(fn):
    pos = (0, 0)
    angle = 0
    for command, value in get_commands(fn):
        direction = (0, 0)
        if command == 'N':
            direction = (0, -1)
        elif command == 'S':
            direction = (0, 1)
        elif command == 'E':
            direction = (1, 0)
        elif command == 'W':
            direction = (-1, 0)
        elif command == 'L':
            angle = (angle - value) % 360
            continue
        elif command == 'R':
            angle = (angle + value) % 360
            continue
        elif command == 'F':
            direction = (int(cos(radians(angle))), int(sin(radians(angle))))
        
        pos = pos[0] + direction[0] * value, pos[1] + direction[1] * value
    
    return pos

x, y = get_final_pos("example1.txt")
assert x + y == 25

x, y = get_final_pos("input.txt")
answer = abs(x) + abs(y)
print("Part 1 =", answer)
assert answer == 562 # check with accepted answer

########
# PART 2

def rotate_ccw(x, y, angle):
    rads = radians(angle)
    sin_angle = int(sin(rads))
    cos_angle = int(cos(rads))

    return x * cos_angle + y * sin_angle, - x * sin_angle + y * cos_angle


def rotate_cw(x, y, angle):
    rads = radians(angle)
    sin_angle = int(sin(rads))
    cos_angle = int(cos(rads))

    return x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle


def get_distance_from(fn):
    ship = (0, 0)
    waypoint = (10, -1)
    for command, value in get_commands(fn):
        #print(command, value, ship, waypoint)
        if command == 'N':
            waypoint = waypoint[0], waypoint[1] - value
        elif command == 'S':
            waypoint = waypoint[0], waypoint[1] + value
        elif command == 'E':
            waypoint = waypoint[0] + value, waypoint[1]
        elif command == 'W':
            waypoint = waypoint[0] - value, waypoint[1]
        elif command == 'L':
            waypoint = rotate_ccw(*waypoint, value)
        elif command == 'R':
            waypoint = rotate_cw(*waypoint, value)
        elif command == 'F':
            ship = ship[0] + waypoint[0] * value, ship[1] + waypoint[1] * value

        #print("\t=", ship, waypoint)
   
    return ship


assert get_distance_from("test-rotation.txt") == (2, 3)


x, y = get_distance_from("example1.txt")
assert x + y == 286


x, y = get_distance_from("input.txt")
answer = abs(x) + abs(y)
print("Part 2 =", answer)
assert answer == 101860 # check with accepted answer

