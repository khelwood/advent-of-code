#!/usr/bin/env python3

import sys
import math

from collections import defaultdict

sys.path.append('..')
from point import Point

def manhattan(p):
    return abs(p[0]) + abs(p[1])

def point_in_spiral(number):
    for p in spiral():
        number -= 1
        if number==0:
            return p

def spiral_dir(pos):
    x,y = pos
    if -x < y < x:
        return (0,1)
    if -y < x <= y:
        return (-1,0)
    if x < y <= -x:
        return (0,-1)
    return (1,0)

def sum_spiral(target):
    vals = defaultdict(int)
    seq = spiral()
    p = next(seq)
    vals[p] = 1
    for p in seq:
        v = sum(vals[p.x+x,p.y+y] for x in range(-1,2) for y in range(-1,2))
        if v > target:
            return v
        vals[p] = v

def spiral():
    pos = Point(0,0)
    yield pos
    while True:
        pos += spiral_dir(pos)
        yield pos

def main():
    if len(sys.argv) <= 1:
        exit("Usage: %s <number>"%sys.argv[0])
    number = int(sys.argv[1])
    p = point_in_spiral(number)
    print("Part 1. distance:", manhattan(p))
    v = sum_spiral(number)
    print("Part 2. value:", v)
    

if __name__ == '__main__':
    main()
