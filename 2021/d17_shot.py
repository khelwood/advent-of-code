#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Target:
    x0: int
    x1: int
    y0: int
    y1: int
    def __contains__(self, p):
        x,y = p
        return (self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1)

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def read_target():
    text = sys.stdin.read().strip()
    pattern = ('target area: x = # .. # , y = # .. #$'
            .replace(' ',r'\s*').replace('#', r'([+-]?\d+)'))
    m = re.match(pattern, text)
    return Target(*map(int, m.groups()))

def track_path(target, vel):
    pos = (0,0)
    height = 0
    while hope(pos, vel, target):
        pos = addp(pos, vel)
        height = max(height, pos[1])
        if pos in target:
            return height
        vel = update_vel(vel)
    return -1

def hope(pos, vel, target):
    if pos[0] > target.x1:
        return False
    if vel[1] <= 0 and pos[1] < target.y0:
        return False
    return True

def update_vel(v):
    vx,vy = v
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    return (vx, vy-1)

def main():
    target = read_target()
    best_height = 0
    count = 0
    yrange = range(min(1, target.y0), max(abs(target.y0), abs(target.y1)))
    for x in range(target.x1+1):
        for y in yrange:
            h = track_path(target, (x,y))
            if h >= 0:
                count += 1
                best_height = max(h, best_height)
    print("best height:", best_height)
    print("count:", count)

# Count: 4656 too low

if __name__ == '__main__':
    main()
