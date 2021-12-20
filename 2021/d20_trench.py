#!/usr/bin/env python3

import sys
from itertools import product

ALL_BITS = 511

def compute_region(light, pos):
    total = 0
    bit = 1
    for nbr in ordered_neighbours(pos):
        if nbr in light:
            total |= bit
        bit <<= 1
    return total

def find_bounds(light):
    x0 = 1_000_000
    x1 = 0
    y0 = 1_000_000
    y1 = 0

    for x,y in light:
        x0 = min(x0, x)
        x1 = max(x1, x)
        y0 = min(y0, y)
        y1 = max(y1, y)

    return (x0,y0,x1,y1)

def enhance(light, bg, code):
    newlight = set()
    if bg=='.':
        newbg = code[0]
    else:
        newbg = code[ALL_BITS]
    x0,y0,x1,y1 = find_bounds(light)

    for pos in product(range(x0-1, x1+2), range(y0-1, y1+2)):
        region = compute_region(light, pos)
        if bg=='#':
            region = ALL_BITS&~region
        if code[region] != newbg:
            newlight.add(pos)

    return newlight, newbg

def ordered_neighbours(pos):
    x,y = pos
    yield (x+1,y+1)
    yield (x,y+1)
    yield (x-1,y+1)
    yield (x+1,y)
    yield (x,y)
    yield (x-1,y)
    yield (x+1,y-1)
    yield (x,y-1)
    yield (x-1,y-1)

def read_input():
    lines = sys.stdin.read().strip().splitlines()
    code = lines.pop(0)
    while not lines[0]:
        del lines[0]

    light = set()
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='#':
                light.add((x,y))
    return code, light

def draw(light, bg):
    x0,y0,x1,y1 = find_bounds(light)
    print("Bounds:", x0, y0, x1, y1)
    for y in range(y0-1, y1+2):
        for x in range(x0-1, x1+2):
            print('#' if ((x,y) in light)==(bg=='.') else '.', end='')
        print()
    print()

def main():
    code, light = read_input()
    bg = '.'
    for _ in range(2):
        light,bg = enhance(light, bg, code)
    print(len(light))
    for _ in range(2, 50):
        light,bg = enhance(light, bg, code)
    print(len(light))

if __name__ == '__main__':
    main()
