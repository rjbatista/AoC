########
# PART 1

def to_seat(code):
    t = code.translate(code.maketrans("BFRL", "1010"))
    r, c = int(t[:7], 2), int(t[7:], 2)

    return r, c, r * 8 + c


# FBFBBFFRLR: row 44, column 5, seat ID 357.
assert to_seat("FBFBBFFRLR") == (44, 5, 357)

# BFFFBBFRRR: row 70, column 7, seat ID 567.
assert to_seat("BFFFBBFRRR") == (70, 7, 567)
# FFFBBBFRRR: row 14, column 7, seat ID 119.
assert to_seat("FFFBBBFRRR") == (14, 7, 119)
# BBFFBBFRLL: row 102, column 4, seat ID 820.
assert to_seat("BBFFBBFRLL") == (102, 4, 820)


with open("event2020/day05/input.txt", "r") as input:
    seats = [to_seat(line) for line in input]


answer = max([id for _, _, id in seats])
print("Part 1 =", answer)
assert answer == 878 # check with accepted answer


########
# PART 2

seats.sort(key = lambda x : x[2])
set_of_seats = {s for _, _, s in seats}
found = [x for x in range(seats[0][2], seats[-1][2]) if x not in set_of_seats][0]
answer = found
print("Part 2 =", answer)
assert answer == 504 # check with accepted answer
