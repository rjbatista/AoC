import re

########
# PART 1

def extra_space(dimensions):
    sortedDimensions = list(dimensions)
    sortedDimensions.sort()

    return sortedDimensions[0] * sortedDimensions[1]


def needed_paper(dimensions):
    l = dimensions[0]
    w = dimensions[1]
    h = dimensions[2]
    # 2*l*w + 2*w*h + 2*h*l
    return 2*l*w + 2*w*h + 2*h*l + extra_space(dimensions)


########
# PART 2

def needed_ribbon(dimensions):
    sortedDimensions = list(dimensions)
    sortedDimensions.sort()
    prod = 1

    for i in sortedDimensions: prod *= i

    return 2*sortedDimensions[0] + 2*sortedDimensions[1] + prod

def main():
    with open('event2015/day02/input.txt') as f:
        totalPaper = 0;
        totalRibbon = 0;

        for line in f:

            dimensions = tuple(int(i) for i in re.match(r"(\d+)x(\d+)x(\d+)", line).groups())

            totalPaper += needed_paper(dimensions)
            totalRibbon += needed_ribbon(dimensions)

            #print("%sx%sx%s=%s" % (dimensions + (neededPaper(dimensions),)))


    print("Part 1 =", totalPaper)
    assert totalPaper == 1598415 # check with accepted answer

    print("Part 2 =", totalRibbon)
    assert totalRibbon == 3812909 # check with accepted answer

main()


