#!/usr/bin/env python3

import sys
import z3

from itertools import combinations
from collections import namedtuple

Machine = namedtuple('Machine', 'lights buttons joltages')

def parse_line(line):
    i = line.index(']')
    lights = [ch=='#' for ch in line[1:i]]
    j = line.index('{')
    buttons = []
    for b in line[i+1:j].strip().split():
        buttons.append({int(s) for s in b[1:-1].split(',')})
    joltages = [int(s) for s in line[j+1:-1].split(',')]
    return Machine(lights, buttons, joltages)

def read_input():
    return list(map(parse_line, filter(bool, map(str.strip, sys.stdin))))

def solve_lights(mac):
    nb = len(mac.buttons)
    for num_on in range(nb+1):
        for bs in combinations(range(nb), num_on):
            state = [False]*len(mac.lights)
            for bi in bs:
                for li in mac.buttons[bi]:
                    state[li] = not state[li]
            if state==mac.lights:
                return num_on
    return None

def solve_joltages(mac):
    sol = z3.Solver()
    bvs = []
    sumbvs = None
    for i in range(len(mac.buttons)):
        bv = z3.Int(f'b{i}')
        sol.add(bv >= 0)
        sumbvs = (bv if sumbvs is None else (sumbvs + bv))
        bvs.append(bv)
    for ji,j in enumerate(mac.joltages):
        expr = None
        for bv,b in zip(bvs, mac.buttons):
            if ji in b:
                expr = (bv if expr is None else (expr + bv))
        sol.add(expr==j)
    best = None
    while sol.check() == z3.sat:
        best = sol.model().evaluate(sumbvs).as_long()
        # Add a constraint to see if we can get a lower solution
        sol.add(sumbvs < best)
    return best

def main():
    macs = read_input()
    print(sum(map(solve_lights, macs)))
    print(sum(map(solve_joltages, macs)))


if __name__ == '__main__':
    main()
