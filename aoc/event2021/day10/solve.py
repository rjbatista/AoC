########
# PART 1

SCORE_CORRUPT = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
ACCEPTED = { '(': ')', '{': '}', '[': ']', '<': '>' }

def read(filename):
    with open("event2021/day10/" + filename, "r") as file:
        return [line.strip() for line in file]


def score_corrupted(line):
    stack = []

    for ch in line:
        if ch in [ '(', '[', '{', '<' ]:
            stack.append(ACCEPTED[ch])

        if ch in [ ')', ']', '}', '>' ]:
            expected = stack.pop()
            if expected != ch:
                return SCORE_CORRUPT[ch], None

    return 0, ''.join(reversed(stack))


# {([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
assert score_corrupted("{([(<{}[<>[]}>{[]{[(<()>")[0] == SCORE_CORRUPT['}']
# [[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
assert score_corrupted("[[<[([]))<([[{}[[()]]]")[0] == SCORE_CORRUPT[')']
# [{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
assert score_corrupted("[{[{({}]{}}([{[{{{}}([]")[0] == SCORE_CORRUPT[']']
# [<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
assert score_corrupted("[<(<(<(<{}))><([]([]()")[0] == SCORE_CORRUPT[')']
# <{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.
assert score_corrupted("<{([([[(<>()){}]>(<<{{")[0] == SCORE_CORRUPT['>']

ex1 = read("example1.txt")
assert sum([score_corrupted(line)[0] for line in ex1]) == 26397

inp = read("input.txt")
answer = sum([score_corrupted(line)[0] for line in inp])
print("Part 1 =", answer)
assert answer == 168417 # check with accepted answer


########
# PART 2

SCORE_MISSING = { ')': 1, ']': 2, '}': 3, '>': 4 }


def score_missing(missing):
    score = 0
    for ch in missing:
        score *= 5
        score += SCORE_MISSING[ch]
    
    return score


# [({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
assert score_corrupted("[({(<(())[]>[[{[]{<()<>>")[1] == '}}]])})]'
# [(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
assert score_corrupted("[(()[<>])]({[<{<<[]>>(")[1] == ')}>]})'
# (((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
assert score_corrupted("(((({<>}<{<{<>}{[]{[]{}")[1] == '}}>}>))))'
# {<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
assert score_corrupted("{<[[]]>}<{[{[{[]{()[[[]")[1] == ']]}}]}]}>'
# <{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.
assert score_corrupted("<{([{{}}[<[[[<>{}]]]>[]]")[1] == '])}>'

# }}]])})] - 288957 total points.
assert score_missing("}}]])})]") == 288957
# )}>]}) - 5566 total points.
assert score_missing(")}>]})") == 5566
# }}>}>)))) - 1480781 total points.
assert score_missing("}}>}>))))") == 1480781
# ]]}}]}]}> - 995444 total points.
assert score_missing("]]}}]}]}>") == 995444
# ])}> - 294 total points.
assert score_missing("])}>") == 294

ex1_missing_scores = sorted([score_missing(missing) for _, missing in [score_corrupted(line) for line in ex1] if missing])
assert ex1_missing_scores[int(len(ex1_missing_scores) / 2)] == 288957

missing_scores = sorted([score_missing(missing) for _, missing in [score_corrupted(line) for line in inp] if missing])
answer = missing_scores[int(len(missing_scores) / 2)]
print("Part 2 =", answer)
assert answer == 2802519786 # check with accepted answer
