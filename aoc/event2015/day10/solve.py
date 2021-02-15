import re

########
# PART 1

'''
1 becomes 11 (1 copy of digit 1).
11 becomes 21 (2 copies of digit 1).
21 becomes 1211 (one 2 followed by one 1).
1211 becomes 111221 (one 1, one 2, and two 1s).
111221 becomes 312211 (three 1s, two 2s, and one 1).
'''

def look_and_say(s, times):
    pattern = re.compile(r"((\d)\2*)")

    for _ in range(times):
        ret = ''
        for match in pattern.finditer(s):
            ret += str(len(match.group(1)))
            ret += match.group(2)
        
        s = ret

    return s


'''
print(lookAndSay('1'))
print(lookAndSay('11'))
print(lookAndSay('21'))
print(lookAndSay('1211'))
print(lookAndSay('1113222113'))
'''

inp = "1113222113"

s = look_and_say(inp, 40)
answer = len(s) 
print("Part 1 =", answer)
assert answer == 252594 # check with accepted answer

########
# PART 2

answer = len(look_and_say(s, 10))
print("Part 2 =", answer)
assert answer == 3579328 # check with accepted answer
