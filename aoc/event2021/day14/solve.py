import re

########
# PART 1

def read(filename):
    with open("event2021/day14/" + filename, "r") as file:
        pattern = re.compile(r"(\w{2}) -> (\w)")

        template = file.readline().strip()

        # skip empty
        file.readline()

        pair_rules = {}
        for line in file:
            match = pattern.match(line)
            if match:
                pair_rules[match[1]] = match[2]
            else:
                raise RuntimeError("invalid input " + line)
    
    return template, pair_rules


def process(template_str : str, pair_rules : dict, times = 1):
    template = list(template_str)

    for _ in range(times):
        pairs = reversed(list(zip(range(len(template)), template, template[1:])))
        for pos, ch1, ch2 in pairs:
            key = ch1 + ch2

            if key in pair_rules:
                template.insert(pos + 1, pair_rules[key])

    return "".join(template)


def difference_of_quantities(template):
    counts = {}
    for ch in template:
        counts[ch] = counts.get(ch, 0) + 1

    count_values = sorted(counts.values())

    return count_values[-1] - count_values[0]


ex1_template, ex1_pair_rules = read("example1.txt")
# After step 1: NCNBCHB
ex1_template = process(ex1_template, ex1_pair_rules)
assert ex1_template == "NCNBCHB"
# After step 2: NBCCNBBBCBHCB
ex1_template = process(ex1_template, ex1_pair_rules)
assert ex1_template == "NBCCNBBBCBHCB"
# After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
ex1_template = process(ex1_template, ex1_pair_rules)
assert ex1_template == "NBBBCNCCNBBNBNBBCHBHHBCHB"
# After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
ex1_template = process(ex1_template, ex1_pair_rules)
assert ex1_template == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"

ex1_template = process(ex1_template, ex1_pair_rules, 10 - 4)

assert difference_of_quantities(ex1_template) == 1588


template, pair_rules = read("input.txt")
template = process(template, pair_rules, 10)
p1_answer = difference_of_quantities(template)
p1_size = len(template)
print("Part 1 =", p1_answer)
assert p1_answer == 2112 # check with accepted answer

########
# PART 2

def apply_counts(template, pair_rules, times = 1):
    current = {}
    counts = {}

    for ch in template:
        counts[ch] = counts.get(ch, 0) + 1

    for ch1, ch2 in zip(template, template[1:]):
        key = ch1 + ch2

        if key in pair_rules:
            current[key] = current.get(key, 0) + 1

    for _ in range(times):
        current_keys = list(current.items())
        for key, value in current_keys:
            if key in pair_rules:
                if value > 0:
                    current[key] -= value
                    rule = pair_rules[key]
                    new_keys = [key[0] + rule, rule + key[1]]

                    counts[rule] = counts.get(rule, 0) + value

                    for new_key in new_keys:
                        current[new_key] = current.get(new_key, 0) + value

    count_values = sorted(counts.values())

    difference =  count_values[-1] - count_values[0]

    return sum(counts.values()), difference


ex1_template, ex1_pair_rules = read("example1.txt")
# use part 1 example to test
assert apply_counts(ex1_template, ex1_pair_rules, 10) == (3073, 1588)

# produces 2188189693529
assert apply_counts(ex1_template, ex1_pair_rules, 40)[1] == 2188189693529

template, pair_rules = read("input.txt")
# use part 1 answer to test
assert apply_counts(template, pair_rules, 10) == (p1_size, p1_answer)

answer = apply_counts(template, pair_rules, 40)[1]
print("Part 2 =", answer)
assert answer == 3243771149914 # check with accepted answer
