import collections

########
# PART 1

def p1_solve_for(num):
    elves = list(range(1, num + 1))

    while len(elves) > 1:
        if len(elves) % 2 == 0:
            elves = elves[::2]
        else:
            elves = elves[::2]
            del elves[0]

    return elves[0]


assert p1_solve_for(5) == 3

answer = p1_solve_for(3004953)
print("Part 1 =", answer)
assert answer == 1815603 # check with accepted answer

########
# PART 2

def p2_solve_for(num):
    l = collections.deque()
    r = collections.deque()
    for i in range(1, num + 1):
        if i < (num // 2) + 1:
            l.append(i)
        else:
            r.appendleft(i)

    while l and r:
        if len(l) > len(r):
            l.pop()
        else:
            r.pop()

        # rotate lists
        r.appendleft(l.popleft())
        l.append(r.pop())

    return l[0] or r[0]

assert p2_solve_for(5) == 2

answer = p2_solve_for(3004953)
print("Part 2 =", answer)
assert answer == 1410630 # check with accepted answer
