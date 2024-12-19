#!/usr/bin/env python3

import sys
import re

def read_input():
    it = iter(sys.stdin)
    towels = next(it).strip().replace(',',' ').split()
    designs = list(filter(bool, map(str.strip, it)))
    return towels, designs

def combine(strings):
    return re.compile('(' + '|'.join(strings) + ')*')

def simplify(towels):
    towels.sort(key=len)
    out = []
    for towel in towels:
        if not combine(out).fullmatch(towel):
            out.append(towel)
    return out

def main():
    towels, designs = read_input()
    simplified = simplify(towels)
    ptn = combine(simplified)
    print(sum(ptn.fullmatch(design) is not None for design in designs))

if __name__ == '__main__':
    main()
