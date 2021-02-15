import re

########
# PART 1

def process_var_names(s):
    return re.sub(r"([a-z]+)", r"_\1", s)


def replace_var_names(s):
    # binary operators
    match = re.search(r"\A(.*) (.*) (.*) -> (.*)", s)

    if (match):
        return "%s %s %s -> %s" % (
            process_var_names(match.group(1)),
            match.group(2),
            process_var_names(match.group(3)),
            process_var_names(match.group(4)))

    # unary operators
    match = re.search(r"\A(?:(.*) )?(.*) -> (.*)", s)

    if match:
        if (match.group(1)):
            return "%s %s -> %s" % (
                match.group(1),
                process_var_names(match.group(2)),
                process_var_names(match.group(3)))
        else:
            return "%s -> %s" % (
                process_var_names(match.group(2)),
                process_var_names(match.group(3)))

    return s


def process(line):
    line = replace_var_names(line)

    line = re.sub(r"(.*) -> (.*)", r"\2 = \1", line)

    line = re.sub(r"AND", "&", line)
    line = re.sub(r"OR", "|", line)
    line = re.sub(r"LSHIFT", "<<", line)
    line = re.sub(r"RSHIFT", ">>", line)
    line = re.sub(r"NOT", r"~", line)

    #print(line)

    return line


def read_code(fn):
    with open('event2015/day07/' + fn, 'r') as f:
        code = []

        for line in f:
            if line[-1] == '\n': line = line[:-1]

            code += [process(line)]

    return code


def run(code):
    to_run = code
    finalVars = {}
    while to_run:
        code = to_run
        to_run = []
        for instr in code:
            try:
                exec(instr)
                #print(instr)

                match = re.search("(.*) =", instr)
                if match:
                    var = match.group(1)
                    value = eval(match.group(1))

                    value = (value + 2**16 if value < 0 else value) & 0xFFFF

                    finalVars[var[1:]] = value
                    #print("found %2s = %s (%d)" % (var[1:], format(value, 'b').zfill(16), value))

            except NameError:
                to_run += [instr]

    return finalVars


assert run(read_code("example1.txt")) == { 'd': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412, 'i': 65079, 'x': 123, 'y': 456 }


code = read_code("input.txt")
answer = run(code)['a']
print("Part 1 =", answer)
assert answer == 956 # check with accepted answer


########
# PART 2

code[89] = "_b = " + str(answer)
answer = run(code)['a']
print("Part 2 =", answer)
assert answer == 40149 # check with accepted answer
