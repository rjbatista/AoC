from collections import deque
from hashlib import md5

########
# PART 1

def is_possible(x, y, ch):
    # wall on edge
    if x < 0 or x > 3:
        return False
    elif y < 0 or y > 3:
        return False

    return True if ch in 'bcdef' else False


def calc_hash(code, path):
    msg = (code + path).encode('utf-8')

    h = md5(msg).hexdigest()

    return h


def find_shortest_path_bfs(code):
    queue = deque([])

    starting_node = 0, 0, ''
    queue.append(starting_node)

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == (3, 3):
            #print("DONE in ", path)
            return path

        ch = calc_hash(code, path)

        for dx, dy, ch, pch in [(0, -1, ch[0], 'U'), (0, 1, ch[1], 'D'), (-1, 0, ch[2], 'L'), (1, 0, ch[3], 'R')]:
            if is_possible(x + dx, y + dy, ch):
                queue.append((x + dx, y + dy, path + pch))

def find_longest_path_bfs(code):
    queue = deque([])

    starting_node = 0, 0, ''
    queue.append(starting_node)

    longest = 0
    while queue:
        x, y, path = queue.popleft()

        if (x, y) == (3, 3):
            longest = max(longest, len(path))
            continue

        ch = calc_hash(code, path)

        for dx, dy, ch, pch in [(0, -1, ch[0], 'U'), (0, 1, ch[1], 'D'), (-1, 0, ch[2], 'L'),
                                (1, 0, ch[3], 'R')]:
            if is_possible(x + dx, y + dy, ch):
                queue.append((x + dx, y + dy, path + pch))

    return longest


# If your passcode were ihgpwlah, the shortest path would be DDRRRD.
assert find_shortest_path_bfs('ihgpwlah') == 'DDRRRD'
# With kglvqrro, the shortest path would be DDUDRLRRUDRD.
assert find_shortest_path_bfs('kglvqrro') == 'DDUDRLRRUDRD'
# With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.
assert find_shortest_path_bfs('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'


answer = find_shortest_path_bfs('ioramepc')
print("Part 1 =", answer)
assert answer == "RDDRULDDRR" # check with accepted answer

########
# PART 2

# If your passcode were ihgpwlah, the longest path would take 370 steps.
assert find_longest_path_bfs('ihgpwlah') == 370
# With kglvqrro, the longest path would be 492 steps long.
assert find_longest_path_bfs('kglvqrro') == 492
# With ulqzkmiv, the longest path would be 830 steps long.
assert find_longest_path_bfs('ulqzkmiv') == 830

answer = find_longest_path_bfs('ioramepc')
print("Part 2 =", answer)
assert answer == 766 # check with accepted answer
