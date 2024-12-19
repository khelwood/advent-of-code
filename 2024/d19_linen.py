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
    out = []
    for towel in sorted(towels, key=len):
        if not combine(out).fullmatch(towel):
            out.append(towel)
    return out

def count_matches(towels, design, cache={'':1}):
    v = cache.get(design)
    if v is not None:
        return v
    c = 0
    for i in range(1, len(design)+1):
        if design[:i] in towels:
            c += count_matches(towels, design[i:])
    cache[design] = c
    return c

def main():
    towels, designs = read_input()
    simplified = simplify(towels)
    ptn = combine(simplified)
    matching_designs = list(filter(ptn.fullmatch, designs))
    print(len(matching_designs))
    towels = set(towels)
    print(sum(count_matches(towels, design) for design in matching_designs))

if __name__ == '__main__':
    main()
