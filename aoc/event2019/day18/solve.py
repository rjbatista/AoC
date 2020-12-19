import heapq 

########
# PART 1

def get_area(fn):
    area = {}
    w, h = 0, 0
    starting_pos = (0, 0)
    with open("event2019/day18/" + fn, "r") as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line[:-1]):
                if ch == '@':
                    starting_pos = (x, y)
                area[x, y] = ch
                w = x
            h = y
    return (w, h), area, starting_pos


def get_possible_paths(area, position):
    to_visit = [(0, position)]
    visited = set()
    paths = []
    while to_visit:
        distance, cur_pos = to_visit.pop(0)
        visited.add(cur_pos)
        x, y = cur_pos

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_pos = x + dx, y + dy
            if new_pos not in visited and new_pos in area:
                ch = area[x + dx, y + dy]

                if ch not in ('#', '.', '@'):
                    paths.append((ch, distance + 1))

                if ch in ('.', '@'):
                    # add to visit
                    to_visit.append((distance + 1, new_pos))

    return paths


def get_all_possible(area):
    all_possible = {}
    for pos, ch in area.items():
        if ch != '#' and ch != '.':
            all_possible[ch] = get_possible_paths(area, pos)

    return all_possible


def get_best_path(all_possible):
    total_keys = len([x for x in all_possible.keys() if 'a' <= x <= 'z'])
    to_visit = []

    already_added = {}
    heapq.heappush(to_visit, (0, '@', []))
    while to_visit:
        steps, pos, haves = heapq.heappop(to_visit)
        possible = all_possible[pos]

        for possibility, distance in possible:
            next_haves = haves

            if 'A' <= possibility <= 'Z':
                if possibility.lower() not in haves:
                    continue
            elif 'a' <= possibility <= 'z':
                if (possibility not in haves):
                    next_haves = haves + [possibility]

            if len(next_haves) == total_keys:
                return steps + distance, next_haves

            key = (possibility, ''.join(sorted(next_haves)))
            if key in already_added and already_added[key] <= steps + distance:
                continue
            else:
                already_added[key] = steps + distance
            
            heapq.heappush(to_visit, (steps + distance, possibility, next_haves))


def get_steps(fn):
    _, area, _ = get_area(fn)
    all_possible = get_all_possible(area)

    return get_best_path(all_possible)


assert get_steps("example1.txt")[0] == 8
assert get_steps("example2.txt")[0] == 86
assert get_steps("example3.txt")[0] == 132
assert get_steps("example4.txt")[0] == 136
assert get_steps("example5.txt")[0] == 81

answer = get_steps("input.txt")
print("Part 1 =", answer)
assert answer[0] == 7048 # check with accepted answer

########
# PART 2

def get_area_p2(fn):
    dimension, area, (x, y) = get_area(fn)
    
    startpos = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            cx, cy = x + dx, y + dy

            if dy == 0 or dx == 0:
                area[cx, cy] = '#'
            else:
                area[cx, cy] = str(len(startpos))
                startpos.append((cx, cy))

    return dimension, area, startpos
    

def get_best_path_p2(all_possible):
    total_keys = len([x for x in all_possible.keys() if 'a' <= x <= 'z'])
    to_visit = []

    already_added = {}
    heapq.heappush(to_visit, (0, [str(x) for x in range(4)], []))
    while to_visit:
        steps, all_pos, haves = heapq.heappop(to_visit)

        for idx, pos in enumerate(all_pos):
            possible = all_possible[pos]
            for possibility, distance in possible:
                next_haves = haves

                if 'A' <= possibility <= 'Z':
                    if possibility.lower() not in haves:
                        continue
                elif 'a' <= possibility <= 'z':
                    if (possibility not in haves):
                        next_haves = haves + [possibility]

                if len(next_haves) == total_keys:
                    return steps + distance, next_haves

                new_all_pos = all_pos[:]
                new_all_pos[idx] = possibility

                key = (tuple(new_all_pos), ''.join(sorted(next_haves)))
                if key in already_added and already_added[key] <= steps + distance:
                    continue
                else:
                    already_added[key] = steps + distance
                
                heapq.heappush(to_visit, (steps + distance, new_all_pos, next_haves))


def get_steps_p2(fn):
    _, area, _ = get_area_p2(fn)
    all_possible = get_all_possible(area)

    return get_best_path_p2(all_possible)


assert get_steps_p2("example1-p2.txt")[0] == 8
assert get_steps_p2("example2-p2.txt")[0] == 24

answer = get_steps_p2("input.txt")
print("Part 2 =", answer)
assert answer[0] == 1836 # check with accepted answer

