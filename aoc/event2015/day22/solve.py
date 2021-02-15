import copy
import heapq
from dataclasses import dataclass
from typing import List

########
# PART 1

_DEBUG = False

'''
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

spell = (name, cost, damage, heal, armor, mana, turns)
'''
'''
spells = [
          { 'name': 'Magic Missile', 'cost': 53, 'damage': 4, 'heal': 0, 'armor': 0, 'mana': 0, 'turns': 0, 'actor': 1, 'applyonce': False },
          { 'name': 'Drain', 'cost': 73, 'damage': 2, 'heal': 2, 'armor': 0, 'mana': 0, 'turns': 0, 'actor': 2, 'applyonce': False },
          { 'name': 'Shield', 'cost': 113, 'damage': 0, 'heal': 0, 'armor': 7, 'mana': 0, 'turns': 6, 'actor': 0, 'applyonce': True },
          { 'name': 'Poison', 'cost': 173, 'damage': 3, 'heal': 0, 'armor': 0, 'mana': 0, 'turns': 6, 'actor': 1, 'applyonce': False },
          { 'name': 'Recharge', 'cost': 229, 'damage': 0, 'heal': 0, 'armor': 0, 'mana': 101, 'turns': 5, 'actor': 0, 'applyonce': False }
        ]
'''
spells = [
          { 'name': 'Recharge', 'cost': 229, 'damage': 0, 'heal': 0, 'armor': 0, 'mana': 101, 'turns': 5, 'actor': 0, 'applyonce': False },
          { 'name': 'Shield', 'cost': 113, 'damage': 0, 'heal': 0, 'armor': 7, 'mana': 0, 'turns': 6, 'actor': 0, 'applyonce': True },
          { 'name': 'Drain', 'cost': 73, 'damage': 2, 'heal': 2, 'armor': 0, 'mana': 0, 'turns': 0, 'actor': 2, 'applyonce': False },
          { 'name': 'Poison', 'cost': 173, 'damage': 3, 'heal': 0, 'armor': 0, 'mana': 0, 'turns': 6, 'actor': 1, 'applyonce': False },
          { 'name': 'Magic Missile', 'cost': 53, 'damage': 4, 'heal': 0, 'armor': 0, 'mana': 0, 'turns': 0, 'actor': 1, 'applyonce': False },
        ]

# order spells by mana cost
spells = list(sorted(spells, key=lambda x: x['cost']))


class Effect:
    def __init__(self, name, damage, heal, armor, recharge, timer, applyonce):
        self.name = name
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.recharge = recharge
        self.timer = timer
        self.applyonce = applyonce


    def cast(self, actor):
        if self.timer > 0:
            actor.effects += [self]

        if (self.applyonce or self.timer == 0):
            self._apply(actor)
            if _DEBUG: print(".")


    def _wearoff(self, actor):
        if (self.applyonce):
            self._apply(actor, reverse=True)


    def apply(self, actor):
        if (not self.applyonce):
            self._apply(actor)
        else:
            if _DEBUG: print("%s is active" % self.name, end="")

        if (self.timer > 0):
            self.timer -= 1

            if _DEBUG: print("; timer is now %d." % self.timer)

            if (self.timer == 0):
                if _DEBUG: print("%s wears off" % self.name)

                self._wearoff(actor)
        else:
            if _DEBUG: print(".")


    def _apply(self, actor, reverse=False):
        if _DEBUG: print("%s " % self.name, end="")

        if (self.damage > 0):
            if _DEBUG: print("deals %d damage" % self.damage, end="")
            actor.hurt(self.damage)

        if (self.heal > 0):
            if _DEBUG: print(" heals %d hit points" % self.heal, end="")
            actor.hit += self.heal

        if (self.armor > 0):
            armor = self.armor if not reverse else -self.armor

            if _DEBUG: print("adds %d armor" % armor, end="")
            actor.armor += armor

        if (self.recharge > 0):
            if _DEBUG: print("recharge %d mana" % self.recharge, end="")
            actor.mana += self.recharge


@dataclass
class Actor:
    ''' basic character '''
    name : str
    hit : int
    damage : int
    armor : int
    effects : List[Effect]

    def applyeffects(self):
        if self.effects:
            for effect in self.effects:
                effect.apply(self)

            self.effects = [effect for effect in self.effects if effect.timer > 0]


    def hurt(self, damage):
        inflicted = max(1, damage - self.armor)

        self.hit = max(0, self.hit - inflicted)

        return inflicted


    def fight(self, opponent):
        inflicted = opponent.hurt(self.damage)

        if _DEBUG: print("%s attacks for %d damage." % (self.name, inflicted))

        return True


    def __eq__(self, x):
        return self.name == x.name and self.hit == x.hit and self.damage == x.damage and self.armor == x.armor and self.effects == x.effects


    def __str__(self):
        return "- %s has %d hit points" % (self.name, self.hit)


@dataclass
class Wizard(Actor):
    ''' wizzard '''
    mana : int
    spentmana : int = 0

    def __str__(self):
        return "- %s has %d hit points, %d armor, %d mana (%d spent)" % (self.name, self.hit, self.armor, self.mana, self.spentmana)


    def __eq__(self, x):
        return super.__eq__(self, x) and self.mana == x.mana and self.spentmana == x.spentmana


    def fight(self, opponent, spell):
        if spell['cost'] > self.mana: return False

        # is effect still active ? if not, add it!
        if (spell['actor'] == 0):
            if spell['name'] in [effect.name for effect in self.effects]:
                return False

            effect = Effect(spell['name'], spell['damage'], spell['heal'], spell['armor'], spell['mana'], spell['turns'], spell['applyonce'])

            if _DEBUG: print("%s casts %s." % (self.name, spell['name']))

            effect.cast(self)

        elif (spell['actor'] == 1):
            if spell['name'] in [effect.name for effect in opponent.effects]:
                return False

            effect = Effect(spell['name'], spell['damage'], spell['heal'], spell['armor'], spell['mana'], spell['turns'], spell['applyonce'])

            if _DEBUG: print("%s casts %s." % (self.name, spell['name']))

            effect.cast(opponent)

        elif (spell['actor'] == 2):
            if spell['name'] in [effect.name for effect in self.effects]:
                return False
            if spell['name'] in [effect.name for effect in opponent.effects]:
                return False

            effect1 = Effect(spell['name'], 0, spell['heal'], spell['armor'], spell['mana'], spell['turns'], spell['applyonce'])
            effect2 = Effect(spell['name'], spell['damage'], 0, spell['armor'], spell['mana'], spell['turns'], spell['applyonce'])

            if _DEBUG: print("%s casts %s." % (self.name, spell['name']))

            effect1.cast(self)
            effect2.cast(opponent)

        # cast
        self.spentmana += spell['cost']
        self.mana -= spell['cost']

        return True


def is_gameover(player, boss):
    if (player.hit == 0):
        # player lost
        return False

    if (boss.hit == 0):
        if _DEBUG: print("Boss DIES!")
        # player won!
        return True

    return None


def doround(player : Actor, boss : Actor, spell, bleeding):
    if _DEBUG: print("\n-- Player turn --")
    if _DEBUG: print(player)
    if _DEBUG: print(boss)

    if bleeding > 0:
        player.hit = max(player.hit - bleeding, 0)

        result = is_gameover(player, boss)
        if (result is not None): return result

    player.applyeffects()
    boss.applyeffects()

    result = is_gameover(player, boss)
    if (result != None): return result

    if (not player.fight(boss, spell)):
        # can't fight - lost
        return False

    result = is_gameover(player, boss)
    if (result != None): return result

    if _DEBUG: print("\n-- Boss turn --")
    if _DEBUG: print(player)
    if _DEBUG: print(boss)

    player.applyeffects()
    boss.applyeffects()

    result = is_gameover(player, boss)
    if (result != None): return result

    boss.fight(player)

    result = is_gameover(player, boss)
    if (result != None): return result

    return None


def spellme(mana):
    for spell in spells:
        if (spell['cost'] <= mana):
            yield spell


class Node(object):
    def __init__(self, player : Wizard, boss : Actor, turn : int):
        self.player = player
        self.boss = boss
        self.turn = turn


    def __lt__(self, x) -> bool:
        if self.turn == x.turn: # advance as quickly as possible to get a min_spent
            if self.boss.hit == x.boss.hit: # with the boss with the lowest health
                return self.player.spentmana < x.player.spentmana # and the least spent mana
            else:
                return self.boss.hit < x.boss.hit
        else:
            return self.turn > x.turn


    def __repr__(self):
        return f"{self.turn}: {self.player.spentmana} player = {self.player.hit} boss = {self.boss.hit}"


def playgame(player, boss, bleeding = 0):
    todo = [Node(player, boss, 0)]
    heapq.heapify(todo)
    #print("\rtrying with spent so far %d..." % (player.spentmana), end="")

    min_spent = 1 << 64
    while todo:
        node = heapq.heappop(todo)
        #print(node)

        if node.player.spentmana >= min_spent:
            continue

        possibilites = spellme(player.mana)
        for each in possibilites:
            newplayer = copy.deepcopy(node.player)
            newboss = copy.deepcopy(node.boss)

            result = doround(newplayer, newboss, each, bleeding)

            if (result == True):
                min_spent = min(min_spent, newplayer.spentmana)
            elif result == None and newplayer.spentmana < min_spent:
                heapq.heappush(todo, Node(newplayer, newboss, node.turn + 1))

    return min_spent

#part1
player = Wizard('Player', 50, 0, 0, [], 500)
boss = Actor('Boss', 58, 9, 0, [])

answer = playgame(player, boss)
print("Part 1 =", answer)
assert answer == 1269 # check with accepted answer

########
# PART 2

player = Wizard('Player', 50, 0, 0, [], 500)
boss = Actor('Boss', 58, 9, 0, [])
answer = playgame(player, boss, 1)
print("Part 2 =", answer)
assert answer == 1309 # check with accepted answer
