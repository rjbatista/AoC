from event2019.day13.computer_v4 import Computer_v4

########
# PART 1
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

with open("event2019/day17/input.txt", "r") as file:
    code = [int(x) for x in file.readline().split(",")]

def read_map(code):
    # setup the brain on a different thread
    computer = Computer_v4(code)
    computer.run()
    return map(chr, computer.get_output())


def get_map(out):
    x, y = 0, 0
    area = {}
    robot_pos = None
    robot_direction = None
    for ch in out:
        if ch == '#':
            area[(x, y)] = ch
        elif ch == '.':
            pass
        elif ch == '\n':
            x = 0
            y += 1
            continue
        else:
            robot_pos = (x, y)
            area[(x, y)] = '#'
            if ch == '^':
                robot_direction = directions[0]
            elif ch == '>':
                robot_direction = directions[1]
            elif ch == 'v':
                robot_direction = directions[2]
            elif ch == '<':
                robot_direction = directions[3]

        x += 1

    return area, robot_pos, robot_direction

def get_pos(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]

def get_valid_direction(area, robot_pos, visited):
    for direction in directions:
        pos = get_pos(robot_pos, direction)
        if pos in area and area[pos] == '#' and pos not in visited:
            return direction

    return None

def get_turn(old_direction, new_direction):
    return {
        0: [],
        1: ['L'],
        2: ['R', 'R'],
        3: ['R']
    }[(directions.index(old_direction) - directions.index(new_direction)) % len(directions)]

def transverse(area, robot_pos, robot_direction):
    visited = set()
    interceptions = []
    direction = get_valid_direction(area, robot_pos, visited)
    current_pos = robot_pos
    path = []
    path += get_turn(robot_direction, direction)
    while direction:
        last_valid_pos = current_pos
        c = 0
        while current_pos in area:
            c += 1
            last_valid_pos = current_pos
            current_pos = get_pos(current_pos, direction)

            if (current_pos in visited):
                interceptions.append(current_pos)
            else:
                visited.add(current_pos)

        current_pos = last_valid_pos
        old_direction = direction
        direction = get_valid_direction(area, last_valid_pos, visited)
        path.append(c - 1)

        if direction != None:
            path += get_turn(old_direction, direction)

    return interceptions, path

def get_alignment_parameters(interceptions):
    return sum([x * y for x, y in interceptions])

out = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
"""
area, robot_pos, robot_direction = get_map(out)
interceptions, _ = transverse(area, robot_pos, robot_direction)
assert get_alignment_parameters(interceptions) == 76

out = read_map(code)
area, robot_pos, robot_direction = get_map(out)
interceptions, path = transverse(area, robot_pos, robot_direction)
answer = get_alignment_parameters(interceptions)
print("Part 1 =", answer)
assert answer == 6244 # check with accepted answer

########
# PART 2
def find_program(path):
    max_group_size = 10

    def replace_all(path, start, size, program):
        pattern = path[start : start + size]
        for i in range(len(path) - size, start - 1, -1):
            if path[i] == pattern[0] and path[i : i + size] == pattern:
                path = path[0:i] + [program] + path[i + size:]

        return path

    for size_A in range(max_group_size, 2, -2):
        pattern_A = path[:size_A]
        path_after_A = replace_all(path, 0, size_A, 'A')
        start_B = 1
        while path_after_A[start_B] == 'A':
            start_B += 1

        for size_B in range(max_group_size, 2, -2):
            pattern_B = path_after_A[start_B : start_B + size_B]
            path_after_B = replace_all(path_after_A, start_B, size_B, 'B')

            start_C = 2
            while path_after_B[start_C] == 'A' or path_after_B[start_C] == 'B':
                start_C += 1

            for size_C in range(2, max_group_size, 2):
                if start_C + size_C >= len(path_after_B):
                    break

                pattern_C = path_after_B[start_C : start_C + size_C]

                path_after_C = replace_all(path_after_B, start_C, size_C, 'C')

                if len(path_after_C) > max_group_size:
                    continue

                is_valid = True
                for ch in path_after_C:
                    if ch not in ['A', 'B', 'C']:
                        is_valid = False
                        break

                if not is_valid:
                    continue

                return path_after_C, pattern_A, pattern_B, pattern_C


def get_chars(program, pattern_A, pattern_B, pattern_C):
    pattern_A = ','.join([str(x) for x in pattern_A])
    pattern_B = ','.join([str(x) for x in pattern_B])
    pattern_C = ','.join([str(x) for x in pattern_C])
    list = []
    for ch in program:
        if ch == 'A':
            list.append(pattern_A)
        elif ch == 'B':
            list.append(pattern_B)
        elif ch == 'C':
            list.append(pattern_C)
    return ','.join(list)

#out = read_map()
program, pattern_A, pattern_B, pattern_C = find_program(path)

inp = []
out = []
inp += [ord(x) for x in ','.join([str(x) for x in program]) + '\n']
inp += [ord(x) for x in ','.join([str(x) for x in pattern_A]) + '\n']
inp += [ord(x) for x in ','.join([str(x) for x in pattern_B]) + '\n']
inp += [ord(x) for x in ','.join([str(x) for x in pattern_C]) + '\n']
inp += [ord(x) for x in "n\n"]

computer = Computer_v4(code)
computer.set_memory_value(0, 2)
computer.run(inp, out)

#print(''.join([chr(x) for x in out[:-1]]))

answer = out[-1]
print("Part 2 =", answer)
assert answer == 1143523 # check with accepted answer
