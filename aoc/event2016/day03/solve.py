import itertools

########
# PART 1

def read_input():
    with open("event2016/day03/input.txt") as f:
        ret = []
        for line in f:
            ret += [[int(x) for x in line.split()]]

        return ret


def is_valid_triangle(triangle):
    for i in itertools.permutations(triangle):
        if (i[0] + i[1] <= i[2]):
            return False

    return True


def solve_for(input):
    count = 0
    total = 0
    for triangle in input:
        total += 1
        count = count + (1 if is_valid_triangle(triangle) else 0)

    return count, total

answer = solve_for(read_input())[0]
print("Part 1 =", answer)
assert answer == 869 # check with accepted answer

########
# PART 2

def read_input_for_p2():
    with open("event2016/day03/input.txt") as f:
        ret = []
        f.readable()
        while True:
            line = f.readline()

            if not line: break;

            l1 = [int(x) for x in line.split()]
            l2 = [int(x) for x in f.readline().split()]
            l3 = [int(x) for x in f.readline().split()]

            for i in range(3):
                ret += [[ l1[i], l2[i], l3[i] ]]

        return ret

answer = solve_for(read_input_for_p2())[0]
print("Part 2 =", answer)
assert answer == 1544 # check with accepted answer
