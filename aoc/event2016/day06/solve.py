########
# PART 1

def read_input():
    with open("event2016/day06/input.txt") as f:
        ret = []
        for line in f:
            ret += [ line[:-1] if line[-1] == '\n' else line ]

    return ret


def solve_for(input, reverse = True):
    all = []
    for word in input:
        if (len(all) < len(word)):
            all += [{} for i in range(len(word) - len(all))]

        for i in range(len(word)):
            if word[i] in all[i]:
                all[i][word[i]] += 1
            else:
                all[i][word[i]] = 0

    result = []
    for pos in all:
        result += [ sorted(pos.items(), key = lambda x : x[1], reverse = reverse)[0][0] ]

    return ''.join(result)

input = [
    'eedadn',
    'drvtee',
    'eandsr',
    'raavrd',
    'atevrs',
    'tsrnev',
    'sdttsa',
    'rasrtv',
    'nssdts',
    'ntnada',
    'svetve',
    'tesnvt',
    'vntsnd',
    'vrdear',
    'dvrsen',
    'enarar',
]

assert solve_for(input) == 'easter'

answer = solve_for(read_input())
print("Part 1 =", answer)
assert answer == "tsreykjj" # check with accepted answer

########
# PART 2

assert solve_for(input, False) == 'advent'

answer = solve_for(read_input(), False)
print("Part 2 =", answer)
assert answer == "hnfbujie" # check with accepted answer
