#!/usr/bin/env python3

import sys

DIRECTIONS = ((0,-1), (-1,0), (1,0), (0,1))

class Cave:
    def __init__(self, lines):
        self.pos_units = {}
        self.lines = tuple(self.extract_units(line, y)
                               for (y,line) in enumerate(lines))
        self.ended = False
        self.deaths = { 'E':0, 'G': 0}
    def __getitem__(self, p):
        return self.pos_units.get(p) or self.lines[p[1]][p[0]]
    def extract_units(self, line, y):
        for x,v in enumerate(line):
            if v=='G':
                self.pos_units[x,y] = Goblin(x,y)
            elif v=='E':
                self.pos_units[x,y] = Elf(x,y)
            else:
                continue
            if isinstance(line, str):
                line = list(line)
            line[x] = '.'
        if isinstance(line, list):
            line = ''.join(line)
        return line
    def display(self):
        yunits = {}
        for (x,y),unit in self.pos_units.items():
            if y not in yunits:
                yunits[y] = [unit]
            else:
                yunits[y].append(unit)
        for y,line in enumerate(self.lines):
            if y in yunits:
                line = list(line)
                for unit in yunits[y]:
                    line[unit.x] = unit.symbol
                line = ''.join(line)
            print(line)
    def retire(self, unit):
        del self.pos_units[unit.position]
        self.ended = not (any(u.symbol=='G' for u in self.pos_units.values())
                     and any(u.symbol=='E' for u in self.pos_units.values()))
        self.deaths[unit.symbol] += 1
    def tick(self):
        for unit in sorted(self.pos_units.values()):
            if self.ended:
                return False
            unit_tick(unit, self)
        return True
    def hp_left(self):
        return sum(u.hp for u in self.pos_units.values() if u.alive)
    def unit_at(self, pos, unit_type):
        u = self.pos_units.get(pos)
        return u if isinstance(u, unit_type) else None

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

class Unit:
    atk = 3
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 200
    @property
    def position(self):
        return (self.x, self.y)
    def __lt__(self, other):
        return (self.y < other.y or self.y==other.y and self.x < other.x)
    @property
    def alive(self):
        return (self.hp > 0)
    @property
    def dead(self):
        return (self.hp <= 0)

class Goblin(Unit):
    symbol = 'G'

class Elf(Unit):
    symbol = 'E'

Goblin.enemy_type = Elf
Elf.enemy_type = Goblin

def nearby(pos, dirs=DIRECTIONS):
    return (addp(pos, d) for d in dirs)

def manhattan(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

def unit_tick(unit, cave, dirs=DIRECTIONS):
    if unit.dead:
        return
    t = find_attack_target(unit, cave)
    if t is None:
        dest = find_move_target(unit, cave)
        if dest is None:
            return False
        newpos = advance(unit, cave, dest)
        del cave.pos_units[unit.position]
        cave.pos_units[newpos] = unit
        unit.x, unit.y = newpos
        if newpos!=dest:
            return True
        t = find_attack_target(unit, cave)
    if t:
        t.hp -= unit.atk
        if t.dead:
            cave.retire(t)
    return True

def find_attack_target(unit, cave):
    target = None
    et = unit.enemy_type
    for n in nearby(unit.position):
        enemy = cave.unit_at(n, et)
        if enemy and (target is None or enemy.hp < target.hp):
            target = enemy
    return target

def find_move_target(unit, cave):
    target_spaces = set()
    et = unit.enemy_type
    for p,u in cave.pos_units.items():
        if isinstance(u, et):
            for n in nearby(p):
                if cave[n]=='.':
                    target_spaces.add(n)
    if not target_spaces:
        return None
    pos = unit.position
    unit.grid = grid = {pos : 0}
    next_steps = [pos]
    reached = set()
    while next_steps and not reached:
        cur_steps = next_steps
        next_steps = []
        for p in cur_steps:
            next_score = grid[p]+1
            for n in nearby(p):
                if n in grid:
                    continue
                if n in target_spaces:
                    reached.add(n)
                    grid[n] = next_score
                    continue
                if cave[n]=='.':
                    grid[n] = next_score
                    next_steps.append(n)
    return min(reached, key=pos_sort_key) if reached else None

def advance(unit, cave, dest):
    if manhattan(unit.position, dest)==1:
        return dest
    old = unit.grid
    unit.grid = grid = {}
    grid[dest] = old[dest]
    next_steps = [dest]
    while next_steps:
        cur_steps = next_steps
        next_steps = []
        for p in cur_steps:
            prev_score = grid[p]-1
            if prev_score < 0:
                continue
            for n in nearby(p):
                if n in grid:
                    continue
                if old.get(n)==prev_score:
                    grid[n] = prev_score
                    next_steps.append(n)
    for n in nearby(unit.position):
        if grid.get(n, 0)==1:
            return n
    return None

def pos_sort_key(a):
    return (a[1],a[0])

def cuttospace(line):
    return line.partition(' ')[0]

def main():
    lines = sys.stdin.read().splitlines()
    cave = Cave(lines)
    turns = 0
    while cave.tick():
        turns += 1
    print("Turns:", turns)
    print("HP left:", cave.hp_left())
    print("Outcome:", turns * cave.hp_left())
    # Part 2
    lose = Elf.atk
    win = 100
    while lose + 1 < win:
        Elf.atk = (win + lose)//2
        cave = Cave(lines)
        turns = 0
        while cave.tick():
            turns += 1
            if cave.deaths['E'] > 0 or cave.ended:
                break
        if cave.deaths['E'] > 0:
            lose = Elf.atk
        else:
            win = Elf.atk
            win_turns = turns
            win_hp = cave.hp_left()
    print("\nBest win:")
    print("Elf attack:", win)
    print("Turns:", win_turns)
    print("HP left:", win_hp)
    print("Outcome:", win_turns*win_hp)

if __name__ == '__main__':
    main()
