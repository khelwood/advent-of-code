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

def sign(n):
    return 1 if n > 0 else (-1) if n < 0 else 0

ORIGIN = Point.at(0,0)
RIGHT,DOWN,LEFT,UP = map(Point, zip((1,0,-1,0), (0,1,0,-1)))

NUMPAD = dict(zip('A0123456789',(ORIGIN, Point.at(-1,0),
    Point.at(-2,-1), Point.at(-1,-1), Point.at(0,-1),
    Point.at(-2,-2), Point.at(-1,-2), Point.at(0,-2),
    Point.at(-2,-3), Point.at(-1,-3), Point.at(0,-3),
)))

DIRPAD = {'A':ORIGIN, UP:LEFT, LEFT:Point.at(-2,1), DOWN:Point.at(-1,1), RIGHT:DOWN}

BIG = 1_000_000_000_000_000

class SingularDict:
    def __init__(self, n):
        self.n = n
    def __getitem__(self, _):
        return self.n

def read_codes():
    return list(filter(bool, map(str.strip, sys.stdin)))

def paths(p):
    u = Point(map(sign, p))
    ax,ay = map(abs, p)
    if ax==0:
        return (ay*(u,),)
    if ay==0:
        return (ax*(u,),)
    vx = ax*(Point.at(u[0], 0),)
    vy = ay*(Point.at(0, u[1]),)
    return (vx+vy, vy+vx)

def calculate_cost(pos, path, valid_positions, master_costs):
    cost = 0
    master_pos = 'A'
    for u in path:
        pos += u
        if pos not in valid_positions:
            return BIG
        cost += master_costs[master_pos, u]
        master_pos = u
    cost += master_costs[master_pos, 'A']
    return cost

def cost_pad(pad, master_costs):
    costs = {}
    valid_positions = set(pad.values())
    for va,vb in product(pad, repeat=2):
        a = pad[va]
        b = pad[vb]
        best_cost = BIG
        for path in paths(b-a):
            cost = calculate_cost(a, path, valid_positions, master_costs)
            if cost < best_cost:
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

def total_complexity(costs, codes):
    total = 0
    for code in codes:
        cost = cost_code(costs, code)
        total += int(code.rstrip('A')) * cost
    return total

def pad_costs(codes, num_middle):
    costs = cost_pad(DIRPAD, SingularDict(1))
    for _ in range(num_middle):
        costs = cost_pad(DIRPAD, costs)
    return cost_pad(NUMPAD, costs)

def main():
    codes = read_codes()
    costs = pad_costs(codes, 1)
    print(total_complexity(costs, codes))
    costs = pad_costs(codes, 24)
    print(total_complexity(costs, codes))
    
if __name__=='__main__':
    main()
