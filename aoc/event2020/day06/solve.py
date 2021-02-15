########
# PART 1

def get_answers(fn):
    with open("event2020/day06/" + fn, "r") as input:
        i = 0
        answers = [(0, {})]
        group_count = 0
        for line in input:
            if line != '\n':
                group_count += 1
                for ch in line[:-1]:
                    _, group_keys = answers[i]
                    group_keys[ch] = group_keys.get(ch, 0) + 1
                    answers[i] = (group_count, group_keys)
            else:
                i += 1
                group_count = 0
                answers.append((0, {}))
    return answers

assert sum([len(group.keys()) for _, group in get_answers("example1.txt")]) == 11

answers = get_answers("input.txt")
answer = sum([len(group) for _, group in answers])
print("Part 1 =", answer)
assert answer == 6416 # check with accepted answer

########
# PART 2

assert sum([1 for group_count, group in get_answers("example1.txt") for _, group_answers in group.items() if group_count == group_answers]) == 6

answer = sum([1 for group_count, group in answers for _, group_answers in group.items() if group_count == group_answers])
print("Part 2 =", answer)
assert answer == 3050 # check with accepted answer
