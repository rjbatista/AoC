import re

########
# PART 1

class Deck:
    def __init__(self, size = 10007):
        self.deck = list(range(size))


    def __repr__(self):
        return str(self.deck)


    def deal(self):
        """
        To deal into new stack, create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly until you run out of cards
        """
        self.deck = self.deck[::-1]

        return self


    def cut(self, n):
        """
        To cut N cards, take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck, retaining their order.
        """
        self.deck = self.deck[n:] + self.deck[:n]

        return self


    def deal_with_increment(self, n):
        """
        To deal with increment N, start by clearing enough space on your table to lay out all of the cards individually in a long line.
        Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card there.
        If you would move into a position past the end of the space on your table, wrap around and keep counting from the leftmost card again.
        Continue this process until you run out of cards.
        """
        old_deck = self.deck[:]
        for i in range(len(self.deck)):
            self.deck[(i * n) % len(old_deck)] = old_deck[i]

        return self


    def load_techniques(self, fn):
        """
        load from file
        """
        with open(fn, "r") as file:
            pattern = re.compile(r"^(deal into new stack|deal with increment|cut)\s*(-?\d*)$")
            for line in file:
                m = pattern.match(line)
                if m:
                    function = m.group(1)
                    if function == 'deal into new stack':
                        self.deal()
                    elif function == 'cut':
                        self.cut(int(m.group(2)))
                    elif function == 'deal with increment':
                        self.deal_with_increment(int(m.group(2)))
                else:
                    raise RuntimeError("invalid input:" + line)

        return self


assert Deck(10).deal().deck == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
assert Deck(10).cut(3).deck == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
assert Deck(10).cut(-4).deck == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
assert Deck(10).deal_with_increment(3).deck == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

assert Deck(10).load_techniques("event2019/day22/example1.txt").deck == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
assert Deck(10).load_techniques("event2019/day22/example2.txt").deck == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
assert Deck(10).load_techniques("event2019/day22/example3.txt").deck == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
assert Deck(10).load_techniques("event2019/day22/example4.txt").deck == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

answer = Deck().load_techniques("event2019/day22/input.txt").deck.index(2019)
print("Part 1 =", answer)
assert answer == 8775 # check with accepted answer

########
# PART 2

# modpow the polynomial: (ax + b)^m % p
# f(x) = (ax + b) % p
# g(x) = (cx + d) % p
# f(f(x)) = a(ax + b)+b = aax + ab+b
# f(g(x)) = a(cx + d)+b = acx + ad+b
def repeat(a, b, n, p):
    if n == 0:
        return 1, 0

    if n % 2 == 0:
        return repeat(a*a % p, (a*b+b) % p, n // 2, p)

    c,d = repeat(a, b, n - 1, p)
    return a*c % p, (a*d+b) % p

class DeckForFollow:
    # using ax + b to calculate the linear transformations
    def __init__(self, size = 119315717514047):
        self.size = size
        self.a = 1
        self.b = 0


    def deal(self):
        """
        To deal into new stack, create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly until you run out of cards
        """
        self.a = -self.a
        self.b = self.size - self.b - 1

        return self


    def cut(self, n):
        """
        To cut N cards, take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck, retaining their order.
        """
        self.b = (self.b + n) % self.size

        return self


    def deal_with_increment(self, n):
        """
        To deal with increment N, start by clearing enough space on your table to lay out all of the cards individually in a long line.
        Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card there.
        If you would move into a position past the end of the space on your table, wrap around and keep counting from the leftmost card again.
        Continue this process until you run out of cards.
        """
        z = pow(n, self.size - 2, self.size) # == modinv(n, L)

        self.a = self.a * z % self.size
        self.b = self.b * z % self.size

        return self


    def __mul__(self, n: int):
        """
        repeated application of the linear transformation
        """
        self.a, self.b = repeat(self.a, self.b, n, self.size)

        return self


    def __getitem__(self, card: int) -> int:
        return (card * self.a + self.b) % self.size


    def load_techniques(self, fn):
        """
        load from file
        """
        with open(fn, "r") as file:
            pattern = re.compile(r"^(deal into new stack|deal with increment|cut)\s*(-?\d*)$")
            lines = file.readlines()
            for line in lines[::-1]:
                m = pattern.match(line)
                if m:
                    function = m.group(1)
                    if function == 'deal into new stack':
                        self.deal()
                    elif function == 'cut':
                        self.cut(int(m.group(2)))
                    elif function == 'deal with increment':
                        self.deal_with_increment(int(m.group(2)))
                else:
                    raise RuntimeError("invalid input:" + line)

        return self


# solve part1 with the new model as a test :)
deck = DeckForFollow(10007).load_techniques("event2019/day22/input.txt")
assert deck[8775] == 2019

answer = (DeckForFollow(119315717514047).load_techniques("event2019/day22/input.txt") * 101741582076661)[2020]
print("Part 2 =", answer)
assert answer == 47141544607176 # check with accepted answer
