#!/usr/bin/env python3

import sys

from collections import defaultdict

def spiral_dir(pos):
    x,y = pos
    if -x < y < x:
        return (0,1)
    if -y < x <= y:
        return (-1,0)
    if x < y <= -x:
        return (0,-1)
    return (1,0)

# Part 1 - figuring out the position of a value in the spiral

def which_square(num):
    i = 0
    while num > (2*i+1)**2:
        i += 1
    return i

def addp(p,d):
    return (p[0]+d[0], p[1]+d[1])

def find_in_square(si, num):
    if si==0:
        return (0,0)
    pos = (si,1-si)
    v = (2*si-1)**2 + 1
    direction = (0,1)
    while v < num:
        pos = addp(pos, spiral_dir(pos))
        v += 1
    return pos        

def position_of(num):
    si = which_square(num)
    return find_in_square(si, num)

def point_in_spiral(number):
    for p in spiral():
        number -= 1
        if number==0:
            return p

# Part 2 - following the spiral

def sum_spiral(target):
    vals = defaultdict(int)
    seq = spiral()
    p = next(seq)
    vals[p] = 1
    for px,py in seq:
        v = sum(vals[px+x, py+y] for x in range(-1,2) for y in range(-1,2))
        if v > target:
            return v
        vals[px,py] = v

def spiral():
    pos = (0,0)
    yield pos
    while True:
        pos = addp(pos, spiral_dir(pos))
        yield pos

# Main
        
def main():
    if len(sys.argv) <= 1:
        exit("Usage: %s <number>"%sys.argv[0])
    number = int(sys.argv[1])
    p = position_of(number)
    print("Part 1. distance:", abs(p[0])+abs(p[1]))
    v = sum_spiral(number)
    print("Part 2. value:", v)
    

if __name__ == '__main__':
    main()
