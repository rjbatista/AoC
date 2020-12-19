import re

########
# PART 1

def get_commands(fn):
    with open("event2020/day14/" + fn) as file:
        pattern = re.compile(r"^(mask|mem)(?:\[(\d+)\])? = ([X10]{36}|\d+)$")
        for line in file:
            m = re.match(pattern, line)
            if m:
                yield m.group(1), m.group(2), m.group(3)
            else:
                raise RuntimeError


def run(fn):
    memory = {}
    mask = ['X'] * 36
    for cmd, address, arg in get_commands(fn):
        if cmd == "mask":
            mask = [int(ch) if ch != 'X' else ch for ch in arg]
            mask.reverse()
        elif cmd == "mem":
            arg = int(arg)
            for i, ch in enumerate(mask):
                if ch == 0:
                    arg &= ~(1 << i)
                elif ch == 1:
                    arg |= (1 << i)
            memory[address] = arg

    #for k, v in memory.items():
    #    print(f"{k}:\t{bin(v)}\t(decimal {v})")

    return memory


assert sum([v for v in run("example1.txt").values()]) == 165


answer = sum([v for v in run("input.txt").values()])
print("Part 1 =", answer)
assert answer == 15919415426101 # check with accepted answer


########
# PART 2
def write_all(memory, address, mask, value):
    try:
        idx = mask.index('X')

        mask[idx] = '0'
        write_all(memory, address, mask, value)
        mask[idx] = '1'
        write_all(memory, address, mask, value)
        mask[idx] = 'X'
    except ValueError:
        for i, ch in enumerate(mask):
            if ch == 1 or ch == '1':
                address |= (1 << i)
            elif ch == '0':
                address &= ~(1 << i)

        memory[address] = value


def run_p2(fn):
    memory = {}
    mask = [0] * 36
    for cmd, address, arg in get_commands(fn):
        if cmd == "mask":
            mask = [int(ch) if ch != 'X' else ch for ch in arg]
            mask.reverse()
        elif cmd == "mem":
            write_all(memory, int(address), mask, int(arg))

    #for k, v in memory.items():
    #    print(f"{k}:\t{bin(v)}\t(decimal {v})")

    return memory


assert sum([v for v in run_p2("example2.txt").values()]) == 208


answer = sum([v for v in run_p2("input.txt").values()])
print("Part 2 =", answer)
assert answer == 3443997590975 # check with accepted answer
