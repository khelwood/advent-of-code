#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Number = namedtuple('Number', 'value y x0 x1')

NUM_PTN = re.compile(r'\d+')

def read_grid(lines):
    symbols = {}
    numbers = []
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch!='.' and not ch.isdigit():
                symbols[x,y] = ch
        for m in re.finditer(NUM_PTN, line):
            value = int(m.group())
            x0 = int(m.start())
            x1 = int(m.end())
            numbers.append(Number(value, y, x0, x1))
    return symbols, numbers

def number_positions(numbers):
    pos = {}
    for n in numbers:
        y = n.y
        for x in range(n.x0, n.x1):
            pos[x,y] = n
    return pos

def adjacent_numbers(pos, number_pos):
    numbers = set()
    px,py = pos
    for y in range(py-1, py+2):
        for x in range(px-1, px+2):
            n = number_pos.get((x,y))
            if n:
                numbers.add(n)
    return numbers

def gear_ratio(symbols, number_pos):
    total = 0
    for pos,ch in symbols.items():
        if ch=='*':
            ns = adjacent_numbers(pos, number_pos)
            if len(ns)==2:
                a,b = ns
                total += a.value * b.value
    return total

def is_part(num, symbols):
    for y in (num.y-1, num.y+1):
        for x in range(num.x0-1, num.x1+1):
            if symbols.get((x,y)):
                return True
    y = num.y
    for x in (num.x0-1, num.x1):
        if symbols.get((x,y)):
            return True
    return False

def main():
    symbols, numbers = read_grid(sys.stdin.read().splitlines())
    total = sum(n.value for n in numbers if is_part(n, symbols))
    print("Part 1:", total)
    number_pos = number_positions(numbers)
    print("Part 2:", gear_ratio(symbols, number_pos))


if __name__ == '__main__':
    main()
