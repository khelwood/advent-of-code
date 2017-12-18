#!/usr/bin/env python3

import sys
import re
import itertools
from collections import namedtuple

class Fighter:
    def __init__(self, hp, attack=0, armour=0):
        self.base_hp = self.hp = hp
        self.base_attack = attack
        self.base_armour = armour
        self.kit = []
    def refresh(self):
        self.hp = self.base_hp
    @property
    def attack(self):
        return self.base_attack + sum(item.attack for item in self.kit)
    @property
    def armour(self):
        return self.base_armour + sum(item.armour for item in self.kit)
    @property
    def alive(self):
        return (self.hp > 0)
    def strike(self, other):
        other.damage(self.attack - other.armour)
    def damage(self, diff):
        if diff > 0:
            self.hp = max(0, self.hp - diff)

Equipment = namedtuple('Equipment', 'name cost attack armour')

def make_equipment(line):
    parts = [x.strip() for x in line.split(':')]
    name = parts[0]
    stats = [int(n) for n in parts[1:]]
    return Equipment(name, *stats)

WEAPONS = """
Dagger:8:4:0
Short sword:10:5:0
Warhammer:25:6:0
Long sword:40:7:0
Great axe:74:8:0
"""

ARMOUR = """
Leather:13:0:1
Chainmail:31:0:2
Splintmail:53:0:3
Bandedmail:75:0:4
Platemail:102:0:5
"""

RINGS = """
Atk 1:25:1:0
Atk 2:50:2:0
Atk 3:100:3:0
Def 1:20:0:1
Def 2:40:0:2
Def 3:80:0:3
"""

WEAPONS = tuple(make_equipment(line) for line in WEAPONS.strip().split('\n'))
ARMOUR = tuple(make_equipment(line) for line in ARMOUR.strip().split('\n'))
RINGS = tuple(make_equipment(line) for line in RINGS.strip().split('\n'))

def kit_choices():
    empty = ((),)
    weapon_choices = ((w,) for w in WEAPONS)
    armour_choices = itertools.chain(empty, ((a,) for a in ARMOUR))
    ring_choices = itertools.chain(empty, ((r,) for r in RINGS),
                                    itertools.combinations(RINGS, 2))
    combined = itertools.product(weapon_choices, armour_choices, ring_choices)
    return (tuple(itertools.chain(*stuff)) for stuff in combined)

def determine_winner(*combatants):
    dmg = [combatants[i].attack - combatants[1-i].armour for i in range(2)]
    if dmg[0] <= 0:
        return -1 if dmg[1]<=0 else 1
    if dmg[1] <= 0:
        return 0
    durations = [(combatants[1-i].hp+dmg[i]-1)//dmg[i] for i in range(2)]
    return 0 if durations[0] <= durations[1] else 1

def main():
    stats = { k: int(v) for k,v in re.findall(r'^([^:]+):\s*([0-9]+)\s*$',
                                              sys.stdin.read(), re.M) }
    boss = Fighter(hp=stats['Hit Points'], attack=stats['Damage'],
                       armour=stats['Armor'])
    player = Fighter(hp=100)
    best_kit_price = sum(x.cost for k in (WEAPONS, ARMOUR, RINGS) for x in k)
    best_kit = None
    worst_kit_price = 0
    worst_kit = None
    for kit in kit_choices():
        player.kit = kit
        kit_price = sum(k.cost for k in kit)
        winner = determine_winner(player, boss)
        if winner==0:
            if kit_price < best_kit_price:
                best_kit_price = kit_price
                best_kit = kit
        if winner==1:
            if kit_price > worst_kit_price:
                worst_kit_price = kit_price
                worst_kit = kit
    print("Cheapest winning kit:", best_kit)
    print(" at price:", best_kit_price)
    print("Most expensive losing kit:", worst_kit)
    print(" at price:", worst_kit_price)

if __name__ == '__main__':
    main()
