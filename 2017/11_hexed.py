#!/usr/bin/env python3

import sys
from collections import Counter

def desc(n, pos, neg):
    if n>0:
        print(n, pos)
    elif n<0:
        print(-n, neg)

def show_final_distance(split_data):
    print("Part 1.")
    moves = Counter(split_data)
    opposites = (('nw', 'se'), ('ne', 'sw'), ('n', 's'))
    for p,n in opposites:
        moves[p] -= moves[n]
        moves[n] = 0
    nw, n, ne = [moves[i] for i in ('nw', 'n', 'ne')]
    if nw>0 and ne>0:
        m = min(nw,ne)
        nw -= m
        ne -= m
        n += m
    elif nw<0 and ne<0:
        m = min(-nw, -ne)
        nw += m
        ne += m
        n -= m
    if n>0 and ne<0:
        m = min(n, -ne)
        n -= m
        ne += m
        nw += m
    if n>0 and nw<0:
        m = min(n, -nw)
        n -= m
        nw += m
        ne += m
    if n<0 and nw>0:
        m = min(-n, nw)
        n += m
        ne -= m
        nw -= m
    if n<0 and ne>0:
        m = min(-n, ne)
        n += m
        ne -= m
        nw -= m
    desc(nw, 'northwest', 'southeast')
    desc(ne, 'northeast', 'southwest')
    desc(n, 'north', 'south')
    print("Total:", abs(nw)+abs(ne)+abs(n)) #781 -- too high

def show_max_distance(split_data):
    n = 0
    nw = 0
    ne = 0
    most_steps = 0
    for d in split_data:
        steps = abs(n)+abs(nw)+abs(ne)
        if steps > most_steps:
            most_steps = steps
        if d=='n':
            if n>=0 and (nw < 0 or ne < 0):
                nw += 1
                ne += 1
                continue
            n += 1
            continue
        if d=='s':
            if n<=0 and (ne > 0 or nw > 0):
                ne -= 1
                nw -= 1
                continue
            n -= 1
            continue
        if d=='ne':
            if ne>=0 and (nw > 0 or n < 0):
                nw -= 1
                n += 1
                continue
            ne += 1
            continue
        if d=='se':
            if nw<=0 and (ne < 0 or n > 0):
                ne += 1
                n -= 1
                continue
            nw -= 1
            continue
        if d=='nw':
            if nw>=0 and (ne > 0 or n < 0):
                ne -= 1
                n += 1
                continue
            nw += 1
            continue
        if d=='sw':
            if ne<=0 and (nw < 0 or n > 0):
                nw += 1
                n -= 1
                continue
            ne -= 1
            continue
        raise ValueError(repr(d))
    steps = abs(n)+abs(nw)+abs(ne)
    print("\nPart 2.")
    print("Final position:")
    desc(n, "north", "south")
    desc(nw, "northwest", "southeast")
    desc(ne, "northeast", "southwest")
    if steps > most_steps:
        most_steps = steps
    print("Final distance:",steps)
    print("Greatest distance:", most_steps)
            
    
def main():
    data = sys.stdin.read()
    split_data = data.replace(',',' ').split()
    show_final_distance(split_data)
    show_max_distance(split_data)

if __name__ == '__main__':
    main()
