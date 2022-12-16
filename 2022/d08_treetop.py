#!/usr/bin/env python3

import sys
from itertools import product

def read_trees():
    trees = {}
    for y,line in enumerate(sys.stdin.read().strip().splitlines()):
        for x,ch in enumerate(line):
            trees[x,y] = int(ch)
    return x+1,y+1,trees

def find_visible(w,h,trees):
    visible = set()
    highest = 0
    for x in range(w):
        highest = -1
        for y in range(h):
            p = trees[x,y]
            if p > highest:
                visible.add((x,y))
                highest = p
        highest = -1
        for y in range(h-1, -1, -1):
            p = trees[x,y]
            if p > highest:
                visible.add((x,y))
                highest = p
    for y in range(h):
        highest = -1
        for x in range(w):
            p = trees[x,y]
            if p > highest:
                visible.add((x,y))
                highest = p
        highest = -1
        for x in range(w-1,-1,-1):
            p = trees[x,y]
            if p > highest:
                visible.add((x,y))
                highest = p
    return visible

def add_pos(a,b):
    return (a[0]+b[0], a[1]+b[1])

DIRECTIONS = ((0,1), (0,-1), (1,0), (-1,0))

def scenic_score(trees, p):
    combined_score = 1
    for d in DIRECTIONS:
        score = score_dir(trees, p, d)
        if score==0:
            return 0
        combined_score *= score
    return combined_score

def score_dir(trees, pos, dir):
    h = trees[pos]
    c = 0
    while True:
        pos = add_pos(pos, dir)
        k = trees.get(pos, 10)
        if k < 10:
            c += 1
        if k >= h:
            break
    return c

def main():
    w,h,trees = read_trees()
    visible = find_visible(w,h,trees)
    print("Num visible:", len(visible))
    h = max(scenic_score(trees, p) for p in product(range(w), range(h)))
    print("Best scenic score:", h)

if __name__ == '__main__':
    main()
