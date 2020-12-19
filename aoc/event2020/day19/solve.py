import regex

########
# PART 1

def read_file(fn):
    with open("event2020/day19/" + fn) as file:
        pattern = regex.compile(r'^(\d+): (?:(?:"(\w+)")|(?:((?:\d+ ?)+)(?: \| ((?:\d+ ?)+))?))$')

        # read rules
        rules = {}
        for line in file:
            if line == '\n':
                break

            m = pattern.match(line)
            if m:
                id = int(m.group(1))
                value = m.group(2)
                poss1 = m.group(3)
                poss2 = m.group(4)

                rules[id] = (value, list(map(int, poss1.split(' '))) if poss1 else None, list(map(int, poss2.split(' '))) if poss2 else None, None)
            else:
                raise RuntimeError("invalid input:" + line)

        # read messages
        messages = []
        for line in file:
            messages.append(line[:-1])
    
        return rules, messages


def build_validator(rules, id):
    rule = rules[id]
    ret = None

    if rule[0]:
        ret = rule[0]

    part1 = None    
    if rule[1]:
        part1 = ""
        for subrule in rule[1]:
            part1 += build_validator(rules, subrule)
        ret = part1
    
    part2 = None
    if rule[2]:
        part2 = ""
        for subrule in rule[2]:
            part2 += build_validator(rules, subrule)
        
        ret = f"(?:{part1}|{part2})"

    if rule[3]:
        special = rule[3].replace("\1", part1)
        if part2:
            special = special.replace("\2", part2)

        ret = special


    return ret


rules, messages = read_file("example1.txt")
validator = regex.compile("^" + build_validator(rules, 0) + "$")
assert sum([1 for message in messages if validator.match(message)]) == 2


rules, messages = read_file("input.txt")
validator = regex.compile("^" + build_validator(rules, 0) + "$")
answer = sum([1 for message in messages if validator.match(message)])
print("Part 1 =", answer)
assert answer == 272

########
# PART 2

def update_rules(rules):
    #8: 42 | 42 8
    #rules[8] = (None, [42], [42, 8])
    rules[8] = (None, [42], None, "(?:\1)+") # repeating pattern
    #11: 42 31 | 42 11 31
    #rules[11] = (None, [42, 31], [42, 11, 31])
    rules[11] = (None, [42], [31], "((?:\1)(?1)?(?:\2))") # recursive pattern


rules, messages = read_file("example2.txt")
update_rules(rules)
validator = regex.compile("^" + build_validator(rules, 0) + "$")
assert sum([1 for message in messages if validator.match(message)]) == 12


rules, messages = read_file("input.txt")
update_rules(rules)
validator = regex.compile("^" + build_validator(rules, 0) + "$")
answer = sum([1 for message in messages if validator.match(message)])
print("Part 2 =", answer)
assert answer == 374
