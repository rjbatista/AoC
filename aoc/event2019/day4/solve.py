import re

########
# PART 1

input = range(235741, 706948 + 1)

def is_valid(pw):
    current_ch = '\0'
    has_duplicates = False
    for ch in pw:
        if ch == current_ch:
            has_duplicates = True
        elif ch < current_ch:
            return False

        current_ch = ch
    
    return has_duplicates

assert is_valid("235778")
assert is_valid("111111")
assert is_valid("111123")
assert not is_valid("223450")
assert not is_valid("123789")

count = 0
for val in input:
    count += 1 if is_valid(str(val)) else 0

answer = sum([1 for x in input if is_valid(str(x))])
print("Part 1 =", answer)
assert answer == 1178 # check with accepted answer

########
# PART 2

def is_valid_p2(pw):
    current_ch = '\0'
    for ch in pw:
        if ch < current_ch:
            return False

        current_ch = ch

    return re.match(r".*(\d)\1.*", re.sub(r'(\d)\1{2,}', '', pw))

assert is_valid_p2("112233")
assert not is_valid_p2("123444")
assert is_valid_p2("111122")
assert is_valid_p2("344455")

answer = sum([1 for x in input if is_valid_p2(str(x))])
print("Part 2 =", answer)
assert answer == 763 # check with accepted answer
