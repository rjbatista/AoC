########
# PART 1

def read_file(fn):
    with open("event2020/day22/" + fn) as file:
        all = [line[:-1] for line in file]
        middle = len(all) // 2

        return list(map(int, all[1:middle])), list(map(int, all[middle + 2:]))


def round(player1, player2):
    c1 = player1.pop(0)
    c2 = player2.pop(0)

    if c1 > c2:
        player1 += [c1, c2]
    else:
        player2 += [c2, c1]


def get_winning_game(player1, player2):
    while True:
        round(player1, player2)

        if not player1:
            return player2

        if not player2:
            return player1


def get_winning_score(game):
    no_cards = len(game)

    return sum([card * (no_cards - idx) for idx, card in enumerate(game)])


assert get_winning_score(get_winning_game(*read_file("example1.txt"))) == 306

answer = get_winning_score(get_winning_game(*read_file("input.txt")))
print("Part 1 =", answer)
assert answer == 32677 # check with accepted answer

########
# PART 2

def is_player1_winner(player1, player2):
    already_played = set()

    while True:
        key = str(player1) + str(player2)

        # if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1.
        if key in already_played:
            return True

        c1 = player1.pop(0)
        c2 = player2.pop(0)

        if len(player1) >= c1 and len(player2) >= c2:
            player1_wins = is_player1_winner(player1[:c1], player2[:c2])
        else:
            player1_wins = c1 > c2

        if player1_wins:
            player1 += [c1, c2]
        else:
            player2 += [c2, c1]

        if not player1:
            return False

        if not player2:
            return True

        already_played.add(key)


def get_winning_game_p2(player1, player2):
    return player1 if is_player1_winner(player1, player2) else player2


assert get_winning_score(get_winning_game_p2(*read_file("example1.txt"))) == 291

players = read_file("input.txt")
#elapsed = timeit.timeit(lambda: cProfile.run("answer = get_winning_score(get_winning_game_p2(*players))"), number = 1)
answer = get_winning_score(get_winning_game_p2(*players))
print("Part 2 =", answer)
assert answer == 33661 # check with accepted answer
