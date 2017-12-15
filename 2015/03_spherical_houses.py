#!/usr/bin/env python3

import sys

sys.path.append('..')

from point import Point

DIRS = { '>': Point(1,0), '<': Point(-1,0), '^': Point(0,1), 'v': Point(0,-1) }

def steps_houses(steps):
    cur = Point(0,0)
    houses = { cur }
    for ch in steps:
        d = DIRS.get(ch)
        if d is not None:
            cur += d
        houses.add(cur)
    return houses

def robo_steps_houses(steps):
    cur = 2*[Point(0,0)]
    houses = { cur[0] }
    i = 0
    for ch in steps:
        d = DIRS.get(ch)
        if d is not None:
            cur[i] += d
            houses.add(cur[i])
            i = 1-i
    return houses

def main():
    steps = sys.stdin.read().strip()
    santa_houses = steps_houses(steps)
    print("Santa houses:", len(santa_houses))
    robo_houses = robo_steps_houses(steps)
    print("Robo-Santa houses:", len(robo_houses))

if __name__ == '__main__':
    main()
