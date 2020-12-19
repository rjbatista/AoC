from event2019.day5.computer import Computer

########
# PART 1


if (__name__ == '__main__'):
    assert Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([0], [])[-1] == 0
    assert Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([33], [])[-1] == 1

    assert Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([0], [])[-1] == 0
    assert Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([33], [])[-1] == 1

    with open("event2019/day5/input.txt", "r") as input:
        code = [int(x) for x in input.readline().split(",")]

    computer = Computer(code)

    answer = computer.run(input = [1])[-1]
    print("Part 1 =", answer)
    assert answer == 7157989 # check with accepted answer

    ########
    # PART 2

    computer = Computer(code)

    answer = computer.run(input = [5])[-1]
    print("Part 2 =", answer)
    assert answer == 7873292 # check with accepted answer
