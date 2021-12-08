import re

########
# PART 1

def read(filename):
    with open("event2021/day08/" + filename, "r") as file:
        pattern = re.compile(r"^((?:(?:\w+) ){10})\|((?: (?:\w+)){4})$")

        lines = []
        for line in file:
            match = pattern.match(line)
            if match:
                lines += [(match[1].split(), match[2].split())]
            else:
                raise RuntimeError("invalid input " + line)

    return lines


def decodable(lines):
    return sum([1 for line in lines for segments in line[1] if len(segments) in [2, 3, 4, 7]])


ex1 = read("example1.txt")
assert decodable(ex1) == 26

inp = read("input.txt")
answer = decodable(inp)
print("Part 1 =", answer)
assert answer == 274 # check with accepted answer


########
# PART 2

def deduce(unique_patterns, without, expected_len):
    return next(x for x in unique_patterns if len(list(filter(lambda c : c not in without, x))) == expected_len)


def decode_line(unique_patterns, output_signals):
    values = ['']*10
    unique_patterns = sorted(unique_patterns, key=lambda x : len(x))

    values[1] = unique_patterns.pop(0)
    values[7] = unique_patterns.pop(0)
    values[4] = unique_patterns.pop(0)
    values[8] = unique_patterns.pop(6)
    # 2 without the segments of 4 has 3 segments on
    values[2] = deduce(unique_patterns[0:3], values[4], 3)
    unique_patterns.remove(values[2])
    # 3 without the segments of 2 has 1 segments on
    values[3] = deduce(unique_patterns[0:3], values[2], 1)
    unique_patterns.remove(values[3])
    values[5] = unique_patterns.pop(0)
    # 9 without the segments of 3 has 1 segments on
    values[9] = deduce(unique_patterns, values[3], 1)
    unique_patterns.remove(values[9])
    # 0 without the segments of 7 has 3 segments on
    values[0] = deduce(unique_patterns, values[7], 3)
    unique_patterns.remove(values[0])
    values[6] = unique_patterns.pop()

    key = { "".join(sorted(list(v))) : i for i, v in enumerate(values) }

    val = 0
    for signal in output_signals:
        val = val * 10 + key["".join(sorted(list(signal)))]

    return val


def decode(lines):
    return sum(decode_line(line[0], line[1]) for line in lines)


assert decode_line(["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"], ["cdfeb", "fcadb", "cdfeb", "cdbaf"]) == 5353

assert decode(ex1) == 61229

answer = decode(inp)
print("Part 2 =", answer)
assert answer == 1012089 # check with accepted answer
