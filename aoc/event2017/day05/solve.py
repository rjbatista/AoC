########
# PART 1

def read(filename):
    with open("event2017/day05/" + filename, "r") as file:
        return [int(offset.strip()) for offset in file.readlines()]


def dump_code(ip, code):
    print(code)
    for p, c in enumerate(code):
        if ip == p:
            print("\033[4m" + str(c) + "\033[0m", end="\t")
        else:
            print(c, end="\t")
    print()


def run(offsets, print_code = False):
    ip = 0
    code = offsets[:]
    steps = 0

    while ip < len(code):
        steps += 1
        if print_code:
            dump_code(ip, code)
        offset = code[ip]
        code[ip] += 1
        ip += offset


    return steps


ex1 = read("example1.txt")
assert run(ex1) == 5

inp = read("input.txt")
answer = run(inp)
print("Part 1 =", answer)
assert answer == 326618 # check with accepted answer


########
# PART 2

def run_p2(offsets, print_code = False):
    ip = 0
    code = offsets[:]
    steps = 0

    while ip < len(code):
        steps += 1
        if print_code:
            dump_code(ip, code)
        offset = code[ip]
        code[ip] += 1 if offset < 3 else -1
        ip += offset


    return steps


assert run_p2(ex1) == 10

answer = run_p2(inp)
print("Part 2 =", answer)
assert answer == 21841249 # check with accepted answer
