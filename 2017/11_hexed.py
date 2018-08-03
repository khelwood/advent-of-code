#!/usr/bin/env python3

import sys

STEPS = {
    'n': (1,0), 'ne': (1,1), 'nw': (1,-1),
    's': (-1,0), 'se': (-1,1), 'sw': (-1,-1),
}

def main():
    steps = sys.stdin.read().split(',')
    furthest = 0
    n = e = 0
    for step in steps:
        dn,de = STEPS[step]
        n += dn
        e += de
        dist = max(abs(n), abs(e))
        if dist > furthest:
            furthest = dist
    print("Final distance:", dist)
    print("Furthest:", furthest)

if __name__ == '__main__':
    main()
