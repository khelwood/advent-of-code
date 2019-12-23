#!/usr/bin/env python3

import sys

DOOR_BIT = 64
DOOR_S = '#'
START_S = '@'

def neighbours(pos):
    x,y = pos
    yield (x-1, y)
    yield (x, y-1)
    yield (x+1, y)
    yield (x, y+1)

def key_int_add(keys, key):
    return (keys | (1<<key))

def key_int_remove(keys, key):
    return (keys & ~(1<<key))

class Maze:
    def __init__(self, grid, keys, doors, start, width, height):
        self.grid = grid
        self.keys = keys
        self.doors = doors
        self.start = start
        self.width = width
        self.height = height
    def is_door(self, pos):
        return (self.grid.get(pos, 0)&DOOR_BIT)!=0
    def door_int(self, pos):
        i = self.grid.get(pos, 0)
        if (i&DOOR_BIT)==0:
            raise ValueError("Not a door: %r"%pos)
        return (i&(DOOR_BIT-1))

def parse_maze(lines):
    grid = {}
    keydict = {}
    doordict = {}
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value != DOOR_S:
                pos = (x,y)
                if value.isupper():
                    key_index = ord(value) - ord('A')
                    doordict[key_index] = pos
                    value = (DOOR_BIT|key_index)
                elif value.islower():
                    key_index = ord(value) - ord('a')
                    keydict[key_index] = pos
                    value = key_index
                elif value=='@':
                    start = pos
                    value = 0
                else:
                    value = 0
                grid[pos] = value
    height = len(lines)
    width = len(lines[0])
    key_values = sorted(keydict)
    keys = [keydict[k] for k in key_values]
    doors = [doordict[k] for k in key_values]

    maze = Maze(grid, keys, doors, start, width, height)
    maze.start_route = make_routing(grid, start)
    assert set(maze.start_route)==set(maze.grid)
    maze.distances = distances(maze)
    maze.required_keys = find_required_keys(maze)
    return maze

def make_routing(grid, start):
    routes = {start:0}
    new = [start]
    steps = 0
    while new:
        steps += 1
        old = new
        new = []
        for pos in old:
            for nbr in neighbours(pos):
                if nbr in grid and nbr not in routes:
                    routes[nbr] = steps
                    new.append(nbr)
    return routes

def distances(maze):
    nk = len(maze.keys)
    distances = [[None]*nk for i in range(nk)]
    for keya, posa in enumerate(maze.keys):
        dista = distances[keya]
        distances[keya][keya] = 0
        if None not in dista:
            continue
        routes = make_routing(maze.grid, posa)
        for keyb, posb in enumerate(maze.keys):
            if dista[keyb] is None:
                dista[keyb] = routes[posb]
                distances[keyb][keya] = routes[posb]
    return distances

def find_required_keys(maze):
    nk = len(maze.keys)
    required = [0]*nk
    for key, pos in enumerate(maze.keys):
        needed = 0
        steps = maze.start_route[pos]
        while steps > 0:
            for nbr in neighbours(pos):
                if nbr not in maze.grid:
                    continue
                r = maze.start_route[nbr]
                if r < steps:
                    steps = r
                    pos = nbr
                    break
            if maze.is_door(pos):
                needed = key_int_add(needed, maze.door_int(pos))
        required[key] = needed
    return required

def total_distance(maze, at_key, keys_needed, _cache={}):
    if keys_needed==0:
        return 0
    cache_key = (at_key, keys_needed)
    distance = _cache.get(cache_key)
    if distance is not None:
        return distance
    best_distance = (1<<30)
    for key,pos in enumerate(maze.keys):
        if ((1<<key)&keys_needed)==0:
            continue
        if (maze.required_keys[key] & keys_needed):
            continue
        distance = (maze.distances[at_key][key]
                    + total_distance(maze, key, key_int_remove(keys_needed, key)))
        best_distance = min(best_distance, distance)
    _cache[cache_key] = best_distance
    return best_distance

def solve(maze):
    nk = len(maze.keys)
    keys_needed = (1 << nk)-1
    best_distance = (1<<30)
    for key, pos in enumerate(maze.keys):
        if maze.required_keys[key]:
            continue
        distance = (maze.start_route[pos]
                    + total_distance(maze, key, key_int_remove(keys_needed, key)))
        best_distance = min(distance, best_distance)
    return best_distance


def main():
    lines = sys.stdin.read().strip().splitlines()
    maze = parse_maze(lines)
    distance = solve(maze)
    print("Best distance:", distance)

if __name__ == '__main__':
    main()
