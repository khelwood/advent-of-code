#!/usr/bin/env python3

import sys

DIRS = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1, -1), (1, 0), (1, 1))

def adjacent(p):
    x,y = p
    for dx,dy in DIRS:
        yield (x+dx, y+dy)

def remove_count(scores):
    og_len = len(scores)
    check = list(scores)
    for r in check:
        if 0 < scores[r] < 4:
            scores[r] = 0
            for a in adjacent(r):
                if scores.get(a, 0) > 0:
                    scores[a] -= 1
                    check.append(a)
    return og_len - sum(v > 0 for v in scores.values())

def read_rolls():
    rolls = set()
    for y,line in enumerate(sys.stdin.read().strip().splitlines()):
        for x,ch in enumerate(line):
            if ch=='@':
                rolls.add((x,y))
    scores = {r:sum(a in rolls for a in adjacent(r)) for r in rolls}
    return scores

def main():
    scores = read_rolls()
    print(sum((scores[p] < 4) for p in scores))
    print(remove_count(scores))

if __name__ == '__main__':
    main()
