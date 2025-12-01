#!/usr/bin/env python3

import sys

def parse_turn(line):
    if line[0]=='L':
        return - int(line[1:])
    if line[0]=='R':
        return int(line[1:])
    raise ValueError(repr(line))

def count_hits(start, turns):
    c = 0
    v = start
    for t in turns:
        v = (v + t) % 100
        if v == 0:
            c += 1
    return c

def count_turn_passes(v, d):
    if 0 < v+d < 100:
        return 0
    if d > 0:
        return 1 + (d - (100 - v))//100
    if d < 0:
        if v==0:
            return (-d)//100
        return 1 + (-d - v)//100
    return 0

def count_passes(start, turns):
    c = 0
    v = start
    for t in turns:
        c += count_turn_passes(v, t)
        v = (v+t)%100
    return c

def main():
    lines = sys.stdin.read().strip().splitlines()
    turns = [parse_turn(line) for line in lines]
    print(count_hits(50, turns))
    print(count_passes(50, turns))

if __name__ == '__main__':
    main()
