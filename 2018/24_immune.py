#!/usr/bin/env python3

import sys
import re

IMMUNE = 0
INFECTION = 1

class UnitGroup:
    def __init__(self, number, hp, atk, atk_type, ini, weak, immune, team):
        self.number = number
        self.unit_hp = hp
        self.atk = atk
        self.atk_type = atk_type
        self.ini = ini
        self.weak = weak
        self.immune = immune
        self.team = team
    @property
    def active(self):
        return (self.number > 0)
    def damage(self, dmg, dmg_type):
        if dmg_type in self.immune:
            return
        if dmg_type in self.weak:
            dmg *= 2
        units_lost = dmg // self.unit_hp
        self.number -= units_lost
    @property
    def effective_power(self):
        n = self.number
        return 0 if n<=0 else (n*self.atk)
    @property
    def selection_priority(self):
        return (self.effective_power, self.ini)
    def __lt__(self, other):
        return self.selection_priority < other.selection_priority
    def find_target(self, enemies):
        # enemies must be ordered by selection priority
        dtype = self.atk_type
        targets = [e for e in enemies if dtype in e.weak]
        if not targets:
            targets = [e for e in enemies if dtype not in e.immune]
            if not targets:
                return None
        return targets[0]
    #number, hp, atk, atk_type, ini, weak, immune, tea
    def __repr__(self):
        return (f"UnitGroup({self.number}, {self.unit_hp}, "
                  f"{self.atk} {self.atk_type})")

def index_which(lines, predicate):
    return next(i for (i,line) in enumerate(lines) if predicate(line))

unit_ptn = re.compile(
    (r'# units? each with # hit points? .+ attack that does # (.+) damage '
    'at initiative #$').replace('#', '([0-9-]+)').replace(' ',r'\s*'))

susc_ptn = re.compile(r'\(([^()]+)\)')

def read_susceptibility(line):
    weak = set()
    immune = set()
    m = susc_ptn.search(line)
    if not m:
        return weak, immune
    susc = m.group(1)
    pieces = [x.strip() for x in susc.split(';')]
    for piece in pieces:
        if piece.startswith('immune to '):
            for x in piece[10:].split(','):
                immune.add(x.strip().lower())
        elif piece.startswith('weak to '):
            for x in piece[8:].split(','):
                weak.add(x.strip().lower())
        else:
            raise ValueError(repr(susc))
    return weak, immune

def read_unit(line, team):
    m = unit_ptn.match(line)
    if not m:
        raise ValueError(repr(line))
    num, hp, atk, ini = (int(m.group(i)) for i in (1,2,3,5))
    dtype = m.group(4).strip().lower()
    weak, immune = read_susceptibility(line)
    return UnitGroup(num, hp, atk, dtype, ini, weak, immune, team)

def read_units(fin):
    groups = [[], []]
    paren_ptn = re.compile(r'\(([^()]+)\)')
    for line in map(str.strip, fin.read().strip().splitlines()):
        if not line:
            continue
        if line.endswith(':'):
            group = (line.rstrip(': ').lower()=='infection')
            continue
        groups[group].append(read_unit(line, group))
    return groups

def iter_units(xs, ys):
    return sorted(xs + ys, reverse=True)

def iter_units_initiative(xs, ys):
    return sorted(xs + ys, key=lambda x: x.ini, reverse=True)

def fight_round(teams):
    teams[IMMUNE].sort(reverse=True)
    teams[INFECTION].sort(reverse=True)
    targets = [list(team) for team in teams[::-1]]
    for unit in iter_units(*teams):
        enemies = targets[unit.team]
        target = unit.find_target(enemies)
        unit.target = target
        if target:
            enemies.remove(target)
    for unit in iter_units_initiative(*teams):
        if unit.target and unit.active:
            unit.target.damage(unit.effective_power, unit.atk_type)
    for i in (IMMUNE, INFECTION):
        teams[i] = [x for x in teams[i] if x.active]

def run_fight(teams):
    while all(teams):
        fight_round(teams)
        
def main():
    teams = read_units(sys.stdin)
    run_fight(teams)
    winner = INFECTION if teams[INFECTION] else IMMUNE
    print("Winning army:", ['Immune', 'Infection'][winner])
    print("Remaining units:", sum(u.number for u in teams[winner]))

if __name__ == '__main__':
    main()
