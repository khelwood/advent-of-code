#!/usr/bin/env python3

import sys
from itertools import product

class Point(tuple):
    @classmethod
    def at(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for (a,b) in zip(self,p))
    def __sub__(self, p):
        return Point(a-b for (a,b) in zip(self,p))
    def __neg__(self):
        return Point(-a for a in self)
    def unit(self):
        return Point(map(unit, self))
    def d1(self):
        x,y = self
        return abs(x) + abs(y)
    def origin(self):
        return not any(self)

def unit(n):
    return 1 if n > 0 else (-1) if n < 0 else 0

def manhattan(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

ORIGIN = Point.at(0,0)
RIGHT,DOWN,LEFT,UP = map(Point, zip((1,0,-1,0), (0,1,0,-1)))
DIRS = (RIGHT,DOWN,LEFT,UP)
DIR_CH = {RIGHT:'>', LEFT:'<', UP:'^', DOWN:'v', 'A':'A'}

NUMPAD = {'A':ORIGIN}|dict(zip('0123456789',(LEFT,
    Point.at(-2,-1), Point.at(-1,-1), Point.at(0,-1),
    Point.at(-2,-2), Point.at(-1,-2), Point.at(0,-2),
    Point.at(-2,-3), Point.at(-1,-3), Point.at(0,-3),
)))

DIRPAD = {'A':ORIGIN, UP:LEFT, LEFT:Point.at(-2,1), DOWN:Point.at(-1,1), RIGHT:DOWN}

def read_codes():
    return list(filter(bool, map(str.strip, sys.stdin)))


def paths(p, cache={ORIGIN:((),)}):
    v = cache.get(p)
    if v is not None:
        return v
    u = p.unit()
    ax,ay = map(abs, p)
    if ax==0:
        v = (ay*(u,),)
    elif ay==0:
        v = (ax*(u,),)
    else:
        found = []
        ux = Point.at(u[0], 0)
        uy = Point.at(0, u[1])
        for path in paths(p-ux):
            found.append((ux,) + path)
        for path in paths(p-uy):
            found.append((uy,) + path)
        v = tuple(found)
    cache[p] = v
    return v

def path_str(path):
    return ''.join(DIR_CH[ch] for ch in path)

def cost_dirpad(controller_costs):
    costs = {}
    valid_positions = set(DIRPAD.values())
    for a,b in permutations(DIRPAD.values(), 2):
        v = b-a
        best_cost = 1000
        for path in paths(v):
            if path_valid(valid_positions, a, path):
                cost = sum_cost(a, path, controller_costs)
                if cost < best_cost:
                    best_cost = cost
        costs[a,b] = best_cost
    return costs

def cost_dirpad2():
    costs = {}
    valid_positions = set(DIRPAD.values())
    for va,vb in product(DIRPAD, repeat=2):
        a = DIRPAD[va]
        b = DIRPAD[vb]
        best_cost = 100_000
        for path in paths(b-a):
            cost = 0
            pos = a
            valid = True
            for u in path:
                new = pos + u
                if new not in valid_positions:
                    valid = False
                    break
                cost += 1
                pos = new
            cost += 1 # press A
            if valid and cost < best_cost:
                best_cost = cost
        costs[va,vb] = best_cost
    return costs

def cost_dirpad1(master_costs):
    costs = {}
    valid_positions = set(DIRPAD.values())
    for va,vb in product(DIRPAD, repeat=2):
        a = DIRPAD[va]
        b = DIRPAD[vb]
        best_cost = 100_000
        for path in paths(b-a):
            cost = 0
            pos = a
            valid = True
            master_pos = 'A'
            for u in path:
                new = pos + u
                if new not in valid_positions:
                    valid = False
                    break
                cost += master_costs[master_pos, u]
                master_pos = u
                pos = new
            cost += master_costs[master_pos, 'A'] # ???back to A (origin)
            if valid and cost < best_cost:
                best_cost = cost
        costs[va,vb] = best_cost
    return costs

def cost_numpad(master_costs):
    costs = {}
    valid_positions = set(NUMPAD.values())
    for va,vb in product(NUMPAD, repeat=2):
        a = NUMPAD[va]
        b = NUMPAD[vb]
        best_cost = 100_000
        for path in paths(b-a):
            cost = 0
            pos = a
            valid = True
            master_pos = 'A'
            for u in path:
                new = pos + u
                if new not in valid_positions:
                    valid = False
                    break
                cost += master_costs[master_pos,u]
                master_pos = u
                pos = new
            cost += master_costs[master_pos, 'A'] # back to A (origin)
            if valid and cost < best_cost:
                best_cost = cost
        costs[va,vb] = best_cost
    return costs

def cost_code(costs, code):
    pos = 'A'
    cost = 0
    for ch in code:
        cost += costs[pos,ch]
        pos = ch
    return cost

# pad2_costs[a,b] is the number of button presses on pad 3 required
#  to push button b on pad 2, starting from position a
pad2_costs = cost_dirpad2()
# for a,b in pad2_costs:
#     print(f'{DIR_CH[a]} -> {DIR_CH[b]} = {pad2_costs[a,b]}')

pad1_costs = cost_dirpad1(pad2_costs)
# print("\nPAD 1")
# for a,b in pad1_costs:
#     print(f'{DIR_CH[a]} -> {DIR_CH[b]} = {pad1_costs[a,b]}')
numpad_costs = cost_numpad(pad1_costs)
# print("\nNUMPAD")
# for a,b in numpad_costs:
#     print(f'{a} -> {b} = {numpad_costs[a,b]}')

total = 0
for code in read_codes():
    cost = cost_code(numpad_costs, code)
    total += int(code.rstrip('A')) * cost
print(total)
