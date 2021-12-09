########
# PART 1

def read(filename):
    with open("event2017/day09/" + filename, "r") as file:
        return file.readline().strip()


def get_score(text):
    score = 0
    groups = 0
    group_level = 0
    in_garbage = False
    count_garbage = 0
    pos = 0
    while pos < len(text):
        if text[pos] == '!':
            pos += 2
            continue

        if (text[pos] == '<' and not in_garbage):
            in_garbage = True
            pos += 1
            continue
        
        if (text[pos] == '>' and in_garbage):
            in_garbage = False
            pos += 1
            continue

        if not in_garbage:
            if text[pos] == '{':
                groups += 1
                group_level += 1
            elif text[pos] == '}':
                score += group_level
                group_level -= 1
        else:
            count_garbage += 1

        pos += 1

    return groups, score, count_garbage


#{}, 1 group.
assert get_score("{}")[0] == 1
#{{{}}}, 3 groups.
assert get_score("{{{}}}")[0] == 3
#{{},{}}, also 3 groups.
assert get_score("{{},{}}")[0] == 3
#{{{},{},{{}}}}, 6 groups.
assert get_score("{{{},{},{{}}}}")[0] == 6
#{<{},{},{{}}>}, 1 group (which itself contains garbage).
assert get_score("{<{},{},{{}}>}")[0] == 1
#{<a>,<a>,<a>,<a>}, 1 group.
assert get_score("{<a>,<a>,<a>,<a>}")[0] == 1
#{{<a>},{<a>},{<a>},{<a>}}, 5 groups.
assert get_score("{{<a>},{<a>},{<a>},{<a>}}")[0] == 5
#{{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).
assert get_score("{{<!>},{<!>},{<!>},{<a>}}")[0] == 2

#{}, score of 1.
assert get_score("{}")[1] == 1
#{{{}}}, score of 1 + 2 + 3 = 6.
assert get_score("{{{}}}")[1] == 6
#{{},{}}, score of 1 + 2 + 2 = 5.
assert get_score("{{},{}}")[1] == 5
#{{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
assert get_score("{{{},{},{{}}}}")[1] == 16
#{<a>,<a>,<a>,<a>}, score of 1.
assert get_score("{<a>,<a>,<a>,<a>}")[1] == 1
#{{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
assert get_score("{{<ab>},{<ab>},{<ab>},{<ab>}}")[1] == 9
#{{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
assert get_score("{{<!!>},{<!!>},{<!!>},{<!!>}}")[1] == 9
#{{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.
assert get_score("{{<a!>},{<a!>},{<a!>},{<ab>}}")[1] == 3


inp = read("input.txt")
answer = get_score(inp)
print("Part 1 =", answer[1])
assert answer[1] == 10820 # check with accepted answer


########
# PART 2

#<>, 0 characters.
assert get_score("<>")[2] == 0
#<random characters>, 17 characters.
assert get_score("<random characters>")[2] == 17
#<<<<>, 3 characters.
assert get_score("<<<<>")[2] == 3
#<{!>}>, 2 characters.
assert get_score("<{!>}>")[2] == 2
#<!!>, 0 characters.
assert get_score("<!!>")[2] == 0
#<!!!>>, 0 characters.
assert get_score("<!!!>>")[2] == 0
#<{o"i!a,<{i<a>, 10 characters.
assert get_score("<{o\"i!a,<{i<a>")[2] == 10


print("Part 2 =", answer[2])
assert answer[2] == 5547 # check with accepted answer
