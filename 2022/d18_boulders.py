#!/usr/bin/env python3

import sys

def parse_cube(line):
    parts = line.strip().replace(',',' ').split()
    return tuple(map(int, parts))

def neighbours(p):
    x,y,z = p
    return (
        (x+1,y,z),
        (x-1,y,z),
        (x,y+1,z),
        (x,y-1,z),
        (x,y,z+1),
        (x,y,z-1),
    )

def count_surface(cubes):
    cube_set = set()
    hits = 0
    for p in cubes:
        for n in neighbours(p):
            if n in cube_set:
                hits += 1
        cube_set.add(p)
    return 6*len(cubes) - 2*hits

def flood(space, p, mins, maxs, v):
    u = space.get(p, 0)
    stack = [p]
    while stack:
        p = stack.pop()
        if space.get(p, u)!=u:
            continue
        space[p] = v
        for n in neighbours(p):
            if (in_bounds(n, mins, maxs) and space.get(n, u)==u):
                stack.append(n)

def bounds(cubes):
    it = iter(cubes)
    cube = next(it)
    mins = list(cube)
    maxs = list(cube)
    for cube in it:
        for i,v in enumerate(cube):
            mins[i] = min(mins[i], v)
            maxs[i] = max(maxs[i], v)
    return ([v-1 for v in mins], [v+1 for v in maxs])

def in_bounds(p, mins, maxs):
    return all(v0 <= v <= v1 for (v0,v,v1) in zip(mins, p, maxs))

def count_exposed(cubes):
    mins, maxs = bounds(cubes)
    space = {cube:1 for cube in cubes}
    start = tuple(mins)
    flood(space, start, mins, maxs, 2)
    exposed = 0
    for cube in cubes:
        for n in neighbours(cube):
            if space.get(n, 0)==2:
                exposed += 1
    return exposed

def main():
    cubes = [parse_cube(line) for line in sys.stdin.read().strip().splitlines()]
    print(count_surface(cubes))
    print(count_exposed(cubes))

if __name__ == '__main__':
    main()
