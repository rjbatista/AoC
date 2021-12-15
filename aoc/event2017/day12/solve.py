import re

########
# PART 1

def read(filename):
    with open("event2017/day12/" + filename, "r") as file:
        pattern = re.compile(r"^(\d+) <-> ((?:\d+(?:, )?)+)$")

        connections = {}
        for line in file:
            match = pattern.match(line)

            if match:
                src = int(match[1])
                dests = [int(x) for x in match[2].split(", ")]

                for dest in dests:
                    connections[src] = connections.get(src, []) + [ dest ]
            else:
                raise RuntimeError("invalid input " + line)
    
        return connections


def count_connections_to(id : int, connections : dict):
    count = 0

    done = set()
    todo = [ id ]
    while todo:
        cur = todo.pop()
        if cur not in done:
            done.add(cur)

            count += 1
            dests = connections[cur]
            for dest in dests:
                if dest not in done:
                    todo.append(dest)

    return count, done


ex1 = read("example1.txt")
assert count_connections_to(0, ex1)[0] == 6

inp = read("input.txt")
answer = count_connections_to(0, inp)[0]
print("Part 1 =", answer)
assert answer == 169 # check with accepted answer


########
# PART 2

def count_groups(connections : dict):
    todo = set(connections.keys())

    count = 0
    while todo:
        count += 1
        
        cur = todo.pop()
        all_connected = count_connections_to(cur, connections)[1]
        for connected in all_connected:
            todo.discard(connected)

    return count


assert count_groups(ex1) == 2

answer = count_groups(inp)
print("Part 2 =", answer)
assert answer == 179 # check with accepted answer
