#!/usr/bin/env python3

import sys
from collections import Counter
DIRECTIONS = {'e': (2,0), 'w': (-2,0), 'ne': (1, -1), 'nw': (-1,-1),
              'se': (1,1), 'sw': (-1,1)}

def parse_path(line, dirs=DIRECTIONS):
    line = line.strip()
    path = []
    n = len(line)
    i = 0
    while i < n:
        direc = dirs.get(line[i])
        if direc:
            path.append(direc)
            i += 1
        else:
            path.append(dirs[line[i:i+2]])
            i += 2
    return path

def path_end(path, start=(0,0)):
    x,y = start
    for vx,vy in path:
        x += vx
        y += vy
    return (x,y)

def neighbours(pos, vectors=DIRECTIONS.values()):
    x,y = pos
    for vx,vy in vectors:
        yield (x+vx, y+vy)

def advance(flipped):
    neighbour_count = Counter()
    for f in flipped:
        for n in neighbours(f):
            neighbour_count[n] += 1
    return {p for (p,c) in neighbour_count.items()
            if c==2 or (c==1 and p in flipped)}

def main():
    paths = list(map(parse_path, sys.stdin))
    flipped = set()
    for path in paths:
        pos = path_end(path)
        if pos in flipped:
            flipped.remove(pos)
        else:
            flipped.add(pos)
    print("Num tiles flipped:", len(flipped))
    for day in range(100):
        flipped = advance(flipped)
    print("After 100 days:", len(flipped))

if __name__ == '__main__':
    main()
