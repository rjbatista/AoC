########
# PART 1

def print_row(row):
    print(''.join(['.' if x == 0 else '^' for x in row]))


def print_rows(rows):
    for row in rows:
        print_row(row)


def parse_row(row):
    return [0 if x == '.' else 1 for x in row]


def get_row(prev):
    row = []

    pprev = [0] + prev + [0]
    all = zip(pprev[0:], pprev[1:], pprev[2:])

    for l, c, r in all:
        """
        Its left and center tiles are traps, but its right tile is not.
        Its center and right tiles are traps, but its left tile is not.
        Only its left tile is a trap.
        Only its right tile is a trap.
        """
        trap = False
        row += [1 if (l + c == 2 and r == 0)
                or (c + r == 2 and l == 0)
                or (l + c == 0 and r == 1)
                or (c + r == 0 and l == 1) else 0]

    return row


def get_rows(start, h):
    rows = []

    r = start
    for i in range(h):
        rows += [r]
        r = get_row(r)

    return rows


def count_safe(rows):
    return len(rows) * len(rows[0]) - sum(sum(row) for row in rows)


#example1 = parse_row('..^^.')
#rows = get_rows(example1, 3)
#print_rows(rows)
#print(count_safe(rows), "safe tiles")

# example 2
#example2 = parse_row('.^^.^.^^^^')
#rows = get_rows(example2, 10)
#print_rows(rows)
#print(count_safe(rows), "safe tiles")

# part 1
p1 = parse_row('^^^^......^...^..^....^^^.^^^.^.^^^^^^..^...^^...^^^.^^....^..^^^.^.^^...^.^...^^.^^^.^^^^.^^.^..^.^')
rows = get_rows(p1, 40)

answer = count_safe(rows)
print("Part 1 =", answer)
assert answer == 1978 # check with accepted answer

########
# PART 2

rows = get_rows(p1, 400000)

answer = count_safe(rows)
print("Part 2 =", answer)
assert answer == 20003246 # check with accepted answer
