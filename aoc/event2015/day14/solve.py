import re
from itertools import cycle

########
# PART 1

'''
Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.
'''

def process_line(line):
    m = re.match(r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", line)

    return m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))


def process_file(fn):
    with open(fn, 'r') as f:
        ret = {}
        for line in f:
            deer, speed, time, wait = process_line(line)
            ret[deer] = [(speed, time), (0, wait)]

        return ret


def move(deer, time):
    dist = 0
    c = cycle(deer)

    while (time > 0):
        curr = next(c)

        this_run = min(time, curr[1])

        dist += curr[0] * this_run
        time -= this_run

    return dist


def run(deers, t):
    final_dists = []
    for speeds in deers.values():
        dist = move(speeds, t)
        final_dists += [dist]

    return max(final_dists)


deers = {}
deers['comet'] = [(14, 10), (0, 127)]
deers['dancer'] = [(16, 11), (0, 162)]

assert run(deers, 1000) == 1120

deers = process_file("event2015/day14/input.txt")

time = 2503
answer = run(deers, time)
print("Part 1 =", answer)
assert answer == 2655 # check with accepted answer


########
# PART 2

scores = { deer: (0,0) for deer in deers }
for t in range(1, time + 1):
    for deer, speeds in deers.items():
        dist = move(speeds, t)
        scores[deer] = (scores[deer][0], dist)

    first_place = max([dist for (_, (_, dist)) in scores.items()])

    for deer, (score, dist) in scores.items():
        scores[deer] = (score + 1, dist) if dist == first_place else (score, dist)


#print(sorted(scores.items(), key = lambda x: x[1][0], reverse = True))
answer = max([x for x, _ in scores.values()])
print("Part 2 =", answer)
assert answer == 1059 # check with accepted answer
