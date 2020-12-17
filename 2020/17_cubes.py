#!/usr/bin/env python3

import sys

def neighbours(pos):
    x,y,z = pos
    for xx in (x-1, x, x+1):
        for yy in (y-1, y, y+1):
            for zz in (z-1, z, z+1):
                if xx!=x or yy!=y or zz!=z:
                    yield (xx,yy,zz)

def neighbours4d(pos):
    x,y,z,w = pos
    for xx in (x-1, x, x+1):
        for yy in (y-1, y, y+1):
            for zz in (z-1, z, z+1):
                for ww in (w-1, w, w+1):
                    if xx!=x or yy!=y or zz!=z or ww!=w:
                        yield (xx,yy,zz,ww)


def all_neighbours(old, nbrfunc=neighbours):
    found = set()
    for pos in old:
        for n in nbrfunc(pos):
            if n not in old:
                found.add(n)
    return found

def count_neighbours(cubes, pos, nbrfunc=neighbours):
    active = 0
    for nbr in nbrfunc(pos):
        if nbr in cubes:
            active += 1
    return active

def advance(old, nbrfunc=neighbours):
    new = set()
    for pos in old:
        if count_neighbours(old, pos, nbrfunc) in (2,3):
            new.add(pos)
    for pos in all_neighbours(old, nbrfunc):
        if count_neighbours(old, pos, nbrfunc)==3:
            new.add(pos)
    return new

def read_cubes():
    cubes = set()
    for y,line in enumerate(sys.stdin):
        line = line.strip()
        for x,ch in enumerate(line):
            if ch=='#':
                cubes.add((x,y,0))
    return cubes

def main():
    initial_cubes = read_cubes()
    cubes = initial_cubes
    for _ in range(6):
        cubes = advance(cubes)
    print("Cubes after 6 cycles (3D):", len(cubes))

    cubes = {(*p,0) for p in initial_cubes}
    for _ in range(6):
        cubes = advance(cubes, neighbours4d)
    print("Cubes after 6 cycles (4D):", len(cubes))


if __name__ == '__main__':
    main()
