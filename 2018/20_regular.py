#!/usr/bin/env python3

import sys
from collections import defaultdict

from regular_maze import lex, follow

def find_distances(start, doors):
    distances = {start: 0}
    distance = 0
    new = [start]
    while new:
        cur = new
        new = []
        distance += 1
        for pos in cur:
            for n in doors[pos]:
                if n not in distances:
                    distances[n] = distance
                    new.append(n)
    return distances

def main():
    tokens = lex(sys.stdin.read().strip().lstrip('^').rstrip('$'))
    doors = defaultdict(set)
    start = (0,0)
    follow({start}, tokens, doors)
    distances = find_distances(start, doors)
    pos, dist = max(distances.items(), key=lambda x:x[1])
    print("Furthest room:", pos)
    print("Distance:", dist)
    distant_rooms = sum(v >= 1000 for v in distances.values())
    print("Rooms at least 100 doors away:", distant_rooms)

if __name__ == '__main__':
    main()
