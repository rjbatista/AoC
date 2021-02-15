from itertools import combinations

########
# PART 1

#Shop
_DEBUG = False

WEAPONS = [
    #Weapons:    Cost  Damage  Armor
    ('Dagger',      ( 8, 4, 0)),
    ('Shortsword',  (10, 5, 0)),
    ('Warhammer',   (25, 6, 0)),
    ('Longsword',   (40, 7, 0)),
    ('Greataxe',    (74, 8, 0))
]

ARMORS = [
    #Armor:      Cost  Damage  Armor
    ('None',        (  0, 0, 0)),
    ('Leather',     ( 13, 0, 1)),
    ('Chainmail',   ( 31, 0, 2)),
    ('Splintmail',  ( 53, 0, 3)),
    ('Bandedmail',  ( 75, 0, 4)),
    ('Platemail',   (102, 0, 5))
]

RINGS = [
    #Rings:      Cost  Damage  Armor
    ('None',        (  0, 0, 0)),
    ('None',        (  0, 0, 0)),
    ('Damage +1',   ( 25, 1, 0)),
    ('Damage +2',   ( 50, 2, 0)),
    ('Damage +3',   (100, 3, 0)),
    ('Defense +1',  ( 20, 0, 1)),
    ('Defense +2',  ( 40, 0, 2)),
    ('Defense +3',  ( 80, 0, 3))
]

def is_alive(principal):
    return principal[0] > 0


def attack(attacker, defender):
    attack = max(1, attacker[1] - defender[2])

    defender[0] = max(0, defender[0] - attack)

    if _DEBUG: print("hit %d points. Remaining %d hit points." % (attack, defender[0]))

    return


def game(player, boss):
    while (is_alive(player) and is_alive(boss)):
        if _DEBUG: print("Player turn: ", end="")
        attack(player, boss)

        if _DEBUG: print("Boss turn: ", end="")
        if is_alive(boss): attack(boss, player)

    return not is_alive(boss)


def equip_item(player, item):
    player[1] += item[1]
    player[2] += item[2]

    return


def equip(player, weapon, armor, rings):
    cost = 0

    newplayer = player[:]

    cost += weapon[0]
    equip_item(newplayer, weapon)

    if armor:
        cost += armor[0]
        equip_item(newplayer, armor)

    for ring in rings:
        cost += ring[0]
        equip_item(newplayer, ring)


    return cost, newplayer


def play(player, boss, func = lambda x : x):
    validCost = []

    for weapon in WEAPONS:
        weaponStats = weapon[1]

        for armor in ARMORS:
            armorStats = armor[1]

            for selectedRings in combinations(RINGS, 2):
                ringStats = [ring[1] for ring in selectedRings]

                cost, equippedPlayer = equip(player, weaponStats, armorStats, ringStats)

                if func(game(equippedPlayer, boss[:])):
                    validCost += [ cost ]

    return validCost


def read_boss():
    with open("event2015/day21/input.txt", "r") as f:
        return list(map(int, [f.readline().split(':')[1] for _ in range(3)]))


player = [100, 0, 0]
boss = read_boss()
answer = min(play(player, boss))
print("Part 1 =", answer)
assert answer == 121 # check with accepted answer

########
# PART 2

player = [100, 0, 0]
boss = [103, 9, 2]

answer = max(play(player, boss, lambda x : not x))
print("Part 2 =", answer)
assert answer == 201 # check with accepted answer
