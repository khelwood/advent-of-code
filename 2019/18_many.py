#!/usr/bin/env python3

import sys

DOOR_BIT = 64
WALL_S = '#'
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
    def __init__(self, grid, keys, doors, starts, width, height):
        self.grid = grid
        self.keys = keys
        self.doors = doors
        self.starts = starts
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
    starts = []
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value != WALL_S:
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
                    starts.append(pos)
                    value = 0
                else:
                    value = 0
                grid[pos] = value
    height = len(lines)
    width = len(lines[0])
    key_values = sorted(keydict)
    keys = [keydict[k] for k in key_values]
    doors = [doordict[k] for k in key_values]

    maze = Maze(grid, keys, doors, starts, width, height)
    maze.start_route = make_routing(grid, starts)
    assert set(maze.start_route)==set(maze.grid)
    maze.keyzones = find_keyzones(maze)
    maze.distances = distances(maze)
    maze.required_keys = find_required_keys(maze)
    return maze

def make_routing(grid, starts):
    routes = {start:0 for start in starts}
    new = list(starts)
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
        routes = make_routing(maze.grid, (posa,))
        for keyb, posb in enumerate(maze.keys):
            if dista[keyb] is None and posb in routes:
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

def complex_distance(maze, positions, at_key, keys_needed, _cache={}):
    if keys_needed==0:
        return 0
    zone = maze.keyzones[at_key]
    positions = positions[:zone] + (at_key,) + positions[zone+1:]
    cache_key = (positions, keys_needed)
    distance = _cache.get(cache_key)
    if distance is not None:
        return distance
    best_distance = (1<<30)
    for key,pos in enumerate(maze.keys):
        if ((1<<key)&keys_needed)==0:
            continue
        if (maze.required_keys[key] & keys_needed):
            continue
        zone = maze.keyzones[key]
        zonekey = positions[zone]
        if zonekey is not None:
            distance = maze.distances[zonekey][key]
        else:
            distance = maze.start_route[pos]
        distance += complex_distance(maze, positions, key,
                                    key_int_remove(keys_needed, key))
        best_distance = min(best_distance, distance)
    _cache[cache_key] = best_distance
    return best_distance

def index_which(seq, predicate):
    return next(i for (i,item) in enumerate(seq) if predicate(item))

def partition_maze(lines):
    y = index_which(lines, lambda line: (START_S in line))
    line = lines[y]
    x = line.index(START_S)
    lines[y] = line[:x-1] + '###' + line[x+2:]
    line = lines[y-1]
    lines[y-1] = line[:x-1] + '@#@' + line[x+2:]
    line = lines[y+1]
    lines[y+1] = line[:x-1] + '@#@' + line[x+2:]

def find_keyzones(maze):
    nk = len(maze.keys)
    if len(maze.starts)==1:
        return [0] * nk
    zones = [None]*nk
    for zone, start in enumerate(maze.starts):
        routes = make_routing(maze.grid, (start,))
        for key, pos in enumerate(maze.keys):
            if pos in routes:
                zones[key] = zone
    return zones

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

def solve_complex(maze):
    nk = len(maze.keys)
    keys_needed = (1<<nk)-1
    best_distance = (1<<30)
    positions = (None,) * len(maze.starts)
    for key, pos in enumerate(maze.keys):
        if maze.required_keys[key]:
            continue
        distance = (maze.start_route[pos]
            + complex_distance(maze, positions, key,
                        key_int_remove(keys_needed, key)))
        best_distance = min(distance, best_distance)
    return best_distance

def main():
    lines = sys.stdin.read().strip().splitlines()
    maze = parse_maze(lines)
    distance = solve(maze)
    print("Best distance (1):", distance)
    # Part 2
    partition_maze(lines)
    maze = parse_maze(lines)
    distance = solve_complex(maze)
    print("Best distance (2):", distance)

if __name__ == '__main__':
    main()
