import re

########
# PART 1
def get_system_from_file(fn):
    system = {}
    pattern = re.compile(r"^(?P<what>\w+)\)(?P<who>\w+)$")
    with open("event2019/day06/" + fn, "r") as input:
        for line in input:
            m = pattern.match(line)
            if m:
                who, what = m.group('who'), m.group('what')

                assert who not in system
                system[who] = what
            else:
                raise RuntimeError
    
    return system

def calculate(system):
    calculated = {}
    todo = set()
    for who, what in system.items():
        todo.add(who)
        todo.add(what)

    todo = list(todo)
    while (todo):
        elem = todo.pop(0)

        if (elem in system):
            parent = system[elem]

            if (parent in calculated):
                calculated[elem] = 1 + calculated[parent]
            else:
                todo.append(elem)
                continue
        else:
            calculated[elem] = 0

    return calculated

calculated = calculate(get_system_from_file("example-input.txt"))
assert sum([y for _,y in calculated.items()]) == 42

calculated = calculate(get_system_from_file("input.txt"))
answer = sum([y for _,y in calculated.items()])
print("Part 1 =", answer)
assert answer == 122782 # check with accepted answer

########
# PART 2

def trace_parents(system, who):
    parents = []
    cur = who
    while (cur):
        if (cur in system):
            parent = system[cur]
            parents += [parent]
            cur = parent
        else:
            cur = None
    
    return parents

def orbits_to(system, f, t):
    from_orbits = trace_parents(system, f)
    to_orbits = trace_parents(system, t)
    to_orbits_set = set(to_orbits)

    count = 0
    while (True):
        cur = from_orbits.pop(0)

        if (cur not in to_orbits_set):
            count += 1
            continue

        count += to_orbits.index(cur)
        break

    return count


system = get_system_from_file("example-input-p2.txt")
assert orbits_to(system, 'YOU', 'SAN') == 4

answer = orbits_to(get_system_from_file("input.txt"), 'YOU', 'SAN')
print("Part 2 =", answer)
assert answer == 271 # check with accepted answer
