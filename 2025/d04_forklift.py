#!/usr/bin/env python3

import sys

def count_adjacent(rolls, p):
    px,py = p
    c = 0
    for x in (px-1,px+1):
        for y in (py-1,py,py+1):
            if (x,y) in rolls:
                c += 1
    if (px,py-1) in rolls:
        c += 1
    if (px,py+1) in rolls:
        c += 1
    return c

def accessible(rolls, p):
    return count_adjacent(rolls, p) < 4

def remove_count(rolls):
    og_len = len(rolls)
    while True:
        removed = set()
        for r in rolls:
            if accessible(rolls, r):
                removed.add(r)
        if not removed:
            break
        rolls -= removed
    return og_len - len(rolls)

def read_rolls():
    rolls = set()
    for y,line in enumerate(sys.stdin.read().strip().splitlines()):
        for x,ch in enumerate(line):
            if ch=='@':
                rolls.add((x,y))
    return rolls

def main():
    rolls = read_rolls()
    print(sum(accessible(rolls, p) for p in rolls))
    print(remove_count(rolls))

if __name__ == '__main__':
    main()
