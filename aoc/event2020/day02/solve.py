import re

########
# PART 1
def is_valid(min_ch, max_ch, ch, pw):
   count = sum([1 if c == ch else 0 for c in pw])

   return min_ch <= count <= max_ch

def get_passwords(fn):
    with open("event2020/day02/" + fn, "r") as input:
        pattern = re.compile(r"^(\d+)-(\d+) (\w): (\w+)$")
        for line in input:
            m = re.match(pattern, line)
            if m:
                min_ch, max_ch = int(m.group(1)), int(m.group(2))
                ch, pw = m.group(3), m.group(4)

                yield (min_ch, max_ch, ch, pw)

assert sum([1 if is_valid(*g) else 0 for g in get_passwords("example1.txt")]) == 2

input = [x for x in get_passwords("input.txt")]
answer = sum([1 if is_valid(*g) else 0 for g in input])
print("Part 1 =", answer)
assert answer == 546 # check with accepted answer

########
# PART 2

def is_valid_p2(first_pos, second_pos, ch, pw):
   count = 1 if pw[first_pos - 1] == ch else 0
   count += 1 if pw[second_pos - 1] == ch else 0

   return count == 1

answer = sum([1 if is_valid_p2(*g) else 0 for g in input])
print("Part 2 =", answer)
assert answer == 275 # check with accepted answer
