#!/usr/bin/env python3

import sys

sys.path.append('..')
from point import Point

NEIGHBOURHOOD = (
    Point(-1,-1), Point(-1,0), Point(-1,1),
    Point(0, -1), Point(0, 1),
    Point(1, -1), Point(1, 0), Point(1, 1),
)
WIDTH = HEIGHT = 100

def load_lines(lines):
    on_lights = set()
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='#':
                on_lights.add((x,y))
    return on_lights

def neighbours(p):
    for d in NEIGHBOURHOOD:
        yield p + d
                
def advance_lights(on, stuck_on=()):
    new = set(stuck_on)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            n = sum((p in on) for p in neighbours((x,y)))
            if n==3 or (n==2 and (x,y) in on):
                new.add((x,y))
    return new

def run_steps(start, steps, stuck_on=()):
    on = set(start)
    on.update(stuck_on)
    for i in range(steps):
        on = advance_lights(on, stuck_on)
        print('', i, end='\r')
    return on

def main():
    steps = 100
    lines = sys.stdin.read().strip().split('\n')
    start_lights = load_lines(lines)
    on = run_steps(start_lights, steps)
    print("Number of lights on:", len(on))
    stuck_on = ((0,0), (0,99), (99,0), (99,99))
    on = run_steps(start_lights, steps, stuck_on)
    print("Number of lights on with four stuck:", len(on))

if __name__ == '__main__':
    main()
