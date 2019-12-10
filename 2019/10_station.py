#!/usr/bin/env python3

import sys
import math
from itertools import combinations
from collections import defaultdict

EMPTY_V = '.'
ASTEROID_V = '#'

def hcf(a,b):
    a = abs(a)
    b = abs(b)
    if b < a:
        a,b = b,a
    while a > 0:
        a,b = b%a, a
    return b

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def subp(a,b):
    return (a[0]-b[0], a[1]-b[1])

def scale(p, x):
    return (p[0]*x, p[1]*x)

def divp(p, d):
    return (p[0]//d, p[1]//d)

def iter_asteroids(data):
    for y, line in enumerate(data.splitlines()):
        for x, ch in enumerate(line):
            if ch!=EMPTY_V:
                yield (x,y)

def can_see(alpha, beta, asteroids):
    path = subp(beta, alpha)
    h = hcf(path[0], path[1])
    if h >= 2:
        v = divp(path, h)
        p = addp(alpha, v)
        while p != beta:
            if p in asteroids:
                return False
            p = addp(p, v)
    return True

def match_routes(asteroids):
    visible = {x:set() for x in asteroids} # exclude self
    for alpha,beta in combinations(asteroids, 2):
        if can_see(alpha, beta, asteroids):
            visible[alpha].add(beta)
            visible[beta].add(alpha)
    return visible

def aim_from(station, asteroids):
    aims = defaultdict(list)
    for target in asteroids:
        v = subp(target, station)
        h = hcf(v[0], v[1])
        if h > 1:
            v = divp(v, h)
        aims[v].append(target)
    def d2(p):
        return -(p[0]-station[0])**2 - (p[1]-station[1])**2
    for v in aims.values():
        v.sort(key=d2)
    return aims

def ordered_angle(p):
    return -math.atan2(p[0], p[1])

def find_destroyed(aims, target_index):
    angles = sorted(aims, key=ordered_angle)
    angle_index = 0
    destroyed = 0
    while destroyed < target_index:
        angle = angles[angle_index]
        line = aims[angle]
        while not line:
            angle_index = (angle_index + 1)%len(angles)
            angle = angles[angle_index]
            line = aims[angle]
        target = line.pop()
        destroyed += 1
        angle_index = (angle_index + 1)%len(angles)
    return target

def main():
    asteroids = set(iter_asteroids(sys.stdin.read().strip()))
    routes = match_routes(asteroids)
    most_visible = max(map(len, routes.values()))
    print("Most number visible:", most_visible)
    station = next(k for (k,v) in routes.items() if len(v)==most_visible)
    asteroids.remove(station)
    aims = aim_from(station, asteroids)
    target = find_destroyed(aims, 200)
    print("Last target:", target)

if __name__ == '__main__':
    main()
