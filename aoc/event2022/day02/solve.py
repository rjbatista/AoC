""" Advent of code 2022 - day XX """
from pathlib import Path

########
# PART 1

def read(filename):
    """ read input """
    rounds = []
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line in file.readlines():
            rounds += [line.split()]

    return rounds


def score_round(hand_p1, hand_p2):
    """ calculate the round score, with inputs as the index in the list [rock, paper, scissors] """
    outcomes = [6, 0, 3, 6, 0]

    return outcomes[hand_p2 - hand_p1 + 2] + hand_p2 + 1


def score(rounds):
    """ calculate score for all rounds, assuming rounds are specified as hand for p1 and p2 """
    total_score = 0

    for coded_hand_p1, coded_hand_p2 in rounds:
        hand_p1 = ord(coded_hand_p1) - ord('A')
        hand_p2 = ord(coded_hand_p2) - ord('X')

        total_score += score_round(hand_p1, hand_p2)

    return total_score


ex1 = read("example1.txt")
assert score(ex1) == 15

inp = read("input.txt")
answer = score(inp)
print("Part 1 =", answer)
assert answer == 11449 # check with accepted answer

########
# PART 2


def score_p2(rounds):
    """
    calculate score for all rounds, assuming rounds are specified as:
    - hand for p1
    - strategy for p2 (X lose, Y draw, Z win)
    """
    total_score = 0

    for coded_hand_p1, coded_strat_p2 in rounds:
        hand_p1 = ord(coded_hand_p1) - ord('A')
        strat_p2 = ord(coded_strat_p2) - ord('X')

        if strat_p2 == 0:
            # lose
            hand_p2 = (hand_p1 - 1) % 3
        elif strat_p2 == 1:
            # draw
            hand_p2 = hand_p1
        else:
            # win
            hand_p2 = (hand_p1 + 1) % 3

        total_score += score_round(hand_p1, hand_p2)

    return total_score


assert score_p2(ex1) == 12

answer = score_p2(inp)
print("Part 2 =", answer)
assert answer == 13187 # check with accepted answer
