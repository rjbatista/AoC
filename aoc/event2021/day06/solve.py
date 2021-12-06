########
# PART 1

def read(filename):
    with open("event2021/day06/" + filename, "r") as file:
        fish = [int(x) for x in file.readline().strip().split(",")]
        
    return fish


def run(fish):
    for i in range(len(fish)):
        fish[i] -= 1
        if fish[i] < 0:
            fish[i] = 6
            fish += [8]


ex1_fish = read("example1.txt")

# Initial state: 3,4,3,1,2
assert ex1_fish == [3,4,3,1,2]
# After  1 day:  2,3,2,0,1
run(ex1_fish)
assert ex1_fish == [2,3,2,0,1]
# After  2 days: 1,2,1,6,0,8
run(ex1_fish)
assert ex1_fish == [1,2,1,6,0,8]
# After  3 days: 0,1,0,5,6,7,8
run(ex1_fish)
assert ex1_fish == [0,1,0,5,6,7,8]
# After  4 days: 6,0,6,4,5,6,7,8,8
run(ex1_fish)
assert ex1_fish == [6,0,6,4,5,6,7,8,8]
# After  5 days: 5,6,5,3,4,5,6,7,7,8
run(ex1_fish)
assert ex1_fish == [5,6,5,3,4,5,6,7,7,8]
# After  6 days: 4,5,4,2,3,4,5,6,6,7
run(ex1_fish)
assert ex1_fish == [4,5,4,2,3,4,5,6,6,7]
# After  7 days: 3,4,3,1,2,3,4,5,5,6
run(ex1_fish)
assert ex1_fish == [3,4,3,1,2,3,4,5,5,6]
# After  8 days: 2,3,2,0,1,2,3,4,4,5
run(ex1_fish)
assert ex1_fish == [2,3,2,0,1,2,3,4,4,5]
# After  9 days: 1,2,1,6,0,1,2,3,3,4,8
run(ex1_fish)
assert ex1_fish == [1,2,1,6,0,1,2,3,3,4,8]
# After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
run(ex1_fish)
assert ex1_fish == [0,1,0,5,6,0,1,2,2,3,7,8]
# After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
run(ex1_fish)
assert ex1_fish == [6,0,6,4,5,6,0,1,1,2,6,7,8,8,8]
# After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
run(ex1_fish)
assert ex1_fish == [5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8]
# After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
run(ex1_fish)
assert ex1_fish == [4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8]
# After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
run(ex1_fish)
assert ex1_fish == [3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8]
# After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
run(ex1_fish)
assert ex1_fish == [2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7]
# After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
run(ex1_fish)
assert ex1_fish == [1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8]
# After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
run(ex1_fish)
assert ex1_fish == [0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8]
# After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
run(ex1_fish)
assert ex1_fish == [6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8]

for _ in range(80 - 18):
    run(ex1_fish)

assert len(ex1_fish) == 5934


inp_fish = read("input.txt")
for _ in range(80):
    run(inp_fish)

answer = len(inp_fish)
print("Part 1 =", answer)
assert answer == 377263 # check with accepted answer


########
# PART 2

def simulate(fish, days):
    total_fish = len(fish)
    days_till_birth = [0] * 9

    for each in fish:
        days_till_birth[each] += 1
    
    for _ in range(days):
        births = days_till_birth[0]
        total_fish += births
        days_till_birth = days_till_birth[1:] + [births]
        days_till_birth[6] += births
    
    return total_fish


ex1_fish = read("example1.txt")
assert simulate(ex1_fish, 256) == 26984457539

inp_fish = read("input.txt")
answer = simulate(inp_fish, 256)
print("Part 2 =", answer)
assert answer == 1695929023803 # check with accepted answer
