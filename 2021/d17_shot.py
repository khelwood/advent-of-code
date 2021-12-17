#!/usr/bin/env python3

import sys
import re
import itertools
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

def track_path(target, vel) -> int:
    """Follows the path of the shot.
    If it hits, returns the height at its highest point.
    If it misses, returns -1."""
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
    px,py = pos
    vx,vy = vel
    if px > target.x1:
        return False
    if vx <= 0 and px < target.x0:
        return False
    if vy <= 0 and py < target.y0:
        return False
    return True

def find_vys(ty0, ty1):
    possible_vy = set()
    for vy0 in range(min(1, ty0), max(abs(ty0), abs(ty1))):
        y = 0
        vy = vy0
        while vy > 0 or y >= ty0:
            if ty0 <= y <= ty1:
                possible_vy.add(vy0)
                break
            y += vy
            vy -= 1
    return possible_vy

def find_vxs(tx0, tx1):
    possible_vx = set()
    for vx0 in range(tx1+1):
        x = 0
        vx = vx0
        while vx < tx1 and (vx > 0 or vx >= tx0):
            if tx0 <= x <= tx1:
                possible_vx.add(vx0)
                break
            x += vx
            if vx > 0:
                vx -= 1
    return possible_vx

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
    vxs = find_vxs(target.x0, target.x1)
    vys = find_vys(target.y0, target.y1)
    for v in itertools.product(vxs, vys):
        h = track_path(target, v)
        if h >= 0:
            count += 1
            best_height = max(h, best_height)
    print("best height:", best_height)
    print("count:", count)

if __name__ == '__main__':
    main()
