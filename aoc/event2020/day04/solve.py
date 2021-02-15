import re

########
# PART 1
def get_passports(fn):
    with open("event2020/day04/" + fn, "r") as input:
        i = 0
        passports = [{}]
        for line in input:
            if line != '\n':
                for k, v in re.findall(r"(\w{3}):([^\s]+)", line):
                    passports[i][k] = v
            else:
                i += 1
                passports.append({})
    return passports

assert sum([1 for passport in get_passports("example1.txt") if len({i : passport[i] for i in passport if i != 'cid'}.keys()) == 7]) == 2

answer = sum([1 for passport in get_passports("input.txt") if len({i : passport[i] for i in passport if i != 'cid'}.keys()) == 7])
print("Part 1 =", answer)
assert answer == 213 # check with accepted answer

########
# PART 2

def is_valid(passport):
    if (len({i : passport[i] for i in passport if i != 'cid'}.keys()) != 7):
        return False
    #byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if not (1920 <= int(passport['byr']) <= 2002):
        return False
    #iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if not (2010 <= int(passport['iyr']) <= 2020):
        return False
    #eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not (2020 <= int(passport['eyr']) <= 2030):
        return False
    #hgt (Height) - a number followed by either cm or in:
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    m = re.match(r"^(\d+)(in|cm)$", passport['hgt'])
    if not m:
        return False
    if m.group(2) == 'cm' and not (150 <= int(m.group(1)) <= 193):
        return False
    if m.group(2) == 'in' and not (59 <= int(m.group(1)) <= 76):
        return False
    #hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not re.match(r"^#[0-9a-f]{6}$", passport['hcl']):
        return False
    #ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if not re.match(r"amb|blu|brn|gry|grn|hzl|oth$", passport['ecl']):
        return False
    #pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.match(r"\d{9}$", passport['pid']):
        return False
    #cid (Country ID) - ignored, missing or not.

    return True

assert sum([1 for passport in get_passports("example2.txt") if is_valid(passport)]) == 4

answer = sum([1 for passport in get_passports("input.txt") if is_valid(passport)])
print("Part 2 =", answer)
assert answer == 147 # check with accepted answer
