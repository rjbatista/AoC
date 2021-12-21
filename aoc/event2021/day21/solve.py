from dataclasses import dataclass
from itertools import count
from collections import Counter
import re

########
# PART 1

class Game:
    def __init__(self, filename) -> None:
        self.players = []
        self.dice_rolls = 0
        self.dice = (1 + i % 100 for i in count())
        self.winning_score = 1000

        with open("event2021/day21/" + filename, "r") as file:
            player_pattern = re.compile(r"Player (\d+) starting position: (\d+)")

            for _ in range(2):
                match = player_pattern.match(file.readline())
                if match:
                    self.players.append((int(match[2]) - 1, 0))


    def __roll_dice__(self):
        self.dice_rolls += 1

        return next(self.dice)


    def play(self):
        while True:
            for idx, (position, score) in enumerate(self.players):
                move = sum(self.__roll_dice__() for _ in range(3))
                position = (position + move) % 10
                score = score + (position + 1)
                self.players[idx] = (position, score)

                if score >= self.winning_score:
                    return idx + 1, score, self.players[(idx + 1) % 2][1]


ex = Game("example1.txt")
_, ex_score_win, ex_score_lose = ex.play()
assert ex.dice_rolls * ex_score_lose == 739785

inp = Game("input.txt")
_, score_win, score_lose = inp.play()

answer = inp.dice_rolls * score_lose
print("Part 1 =", answer)
assert answer == 888735 # check with accepted answer

########
# PART 2

@dataclass(frozen=True)
class Node:
    turn: int
    p1_pos: int
    p1_score: int
    p2_pos: int
    p2_score: int


class QuantumGame(Game):
    def __init__(self, filename) -> None:
        super().__init__(filename)

        self.dice_values = Counter((d1 + d2 + d3 for d1 in range(1, 4) for d2 in range(1, 4) for d3 in range(1, 4)))
        self.winning_score = 21

    def play(self):
        games = { Node(0, *self.players[0], *self.players[1]): 1 }

        win_count = [0] * 2
        players = [0] * 2
        scores = [0] * 2

        while games:
            new_games = {}
            for node, games in games.items():
                for move, chances in self.dice_values.items():
                    players = [node.p1_pos, node.p2_pos]
                    scores = [node.p1_score, node.p2_score]

                    players[node.turn] = (players[node.turn] + move) % 10
                    scores[node.turn] = scores[node.turn] + (players[node.turn] + 1)

                    if scores[node.turn] >= self.winning_score:
                        win_count[node.turn] += games * chances
                    else:
                        new_node = Node((node.turn + 1) % 2, players[0], scores[0], players[1], scores[1])

                        if new_node not in new_games:
                            new_games[new_node] = games * chances
                        else:
                            new_games[new_node] += games * chances

            games = new_games

        return win_count
        

ex = QuantumGame("example1.txt")
assert max(ex.play()) == 444356092776315

inp = QuantumGame("input.txt")
answer = max(inp.play())
print("Part 2 =", answer)
assert answer == 647608359455719 # check with accepted answer
