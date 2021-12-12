#!/usr/bin/env python3

import sys
from collections import defaultdict

def read_rooms():
    d = defaultdict(set)
    for line in sys.stdin.read().strip().splitlines():
        x,_,y = line.partition('-')
        d[x].add(y)
        d[y].add(x)
    for r in d['start']:
        d[r].remove('start')
    return d

def iter_paths(rooms, small, can_repeat=False, path=None, visited=None):
    if path is None:
        path = ['start']
        visited = {'start'}
    cur = path[-1]
    options = rooms[cur]
    for r in options:
        rep = can_repeat
        if r in visited:
            if rep:
                rep = False
            else:
                continue
        if r=='end':
            yield path + ['end']
            continue
        nv = visited
        if r in small:
            nv = nv | {r}
        yield from iter_paths(rooms, small, rep, path+[r], nv)

def main():
    rooms = read_rooms()
    small_rooms = {x for x in rooms if x.islower()}
    path_count = sum(1 for path in iter_paths(rooms, small_rooms))
    print("Num paths:", path_count)
    path_count = sum(1 for path in iter_paths(rooms, small_rooms, True))
    print("Num paths with a possible repeat:", path_count)

if __name__ == '__main__':
    main()
