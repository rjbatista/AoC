
########
# PART 1

def draw_set(theset):
    minx,miny,maxx,maxy = 0,0,0,0

    for (x,y) in theset:
        if (x < minx): minx = x
        if (y < miny): miny = y
        if (x > maxx): maxx = x
        if (x > maxy): maxy = y

    print("%3d %s" % (minx,str(maxx).rjust(maxx-minx)))
    for y in range(maxy, miny, -1):
        print("%3d " % y,end="")
        for x in range(minx, maxx):
            print('X' if (x,y) in theset else ' ', end='')
        print('')

    return


def calc(n = 1):
    switcher = {
        '^': (lambda p: (p[0], p[1]+1)),
        'v': (lambda p: (p[0], p[1]-1)),
        '<': (lambda p: (p[0]-1, p[1])),
        '>': (lambda p: (p[0]+1, p[1])),
    }

    turn = 0
    pos = [(0,0)] * n
    visited = set([pos[0]])
    with open('event2015/day03/input.txt') as file:
        for line in file:
            for ch in line:
                pos[turn % n] = switcher[ch](pos[turn % n])
                visited.add(pos[turn % n])
                turn += 1

    #drawset(visited)
    #print ("Total visited: %d" % len(visited))
    return len(visited)

answer = calc()
print("Part 1 =", answer)
assert answer == 2572 # check with accepted answer

########
# PART 2

answer = calc(2)
print("Part 2 =", answer)
assert answer == 2631 # check with accepted answer
