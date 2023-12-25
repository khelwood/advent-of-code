#!/usr/bin/env python3

import sys

DIRECTIONS = {'>': 1, '<': -1, 'v': 1j, '^': -1j}

class Maze:
    def __init__(self, ways, start, end):
        self.ways = ways
        self.start = start
        self.end = end

    def find_junctions(self):
        start_junction = Junction(0, self.start, {})
        pos_junction = {}
        self.junctions = junctions = [start_junction]
        for p, pw in self.ways.items():
            if len(pw) > 2:
                junctions.append(Junction(len(junctions), p, {}))
        end_junction = Junction(len(junctions), self.end, {})
        pos_junction = {j.pos:j for j in junctions}
        pos_junction[end_junction.pos] = end_junction
        for junc in junctions:
            for q in self.ways[junc.pos]:
                path = self.next_junction(junc.pos, q)
                if path:
                    nj = pos_junction[path[-1]]
                    junc.links[nj] = path

    def next_junction(self, start, cur):
        dist = 0
        last = start
        path = [cur]
        while True:
            if cur==self.end:
                return path
            ways = self.ways[cur]
            if len(ways) > 2:
                return path
            p = next((pp for pp in ways if pp!=last), None)
            if p is None:
                return None
            last = cur
            cur = p
            path.append(cur)


class Junction:
    def __init__(self, index, pos, links):
        self.index = index
        self.pos = pos
        self.links = links
        self.bit = (1<<index)

    def __repr__(self):
        return f'Junction({self.index})'


def parse_maze(lines, respect_slopes):
    ways = {}
    hei = len(lines)
    wid = len(lines[0])
    path_chars = {'.'}
    if not respect_slopes:
        path_chars |= DIRECTIONS.keys()
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            p = complex(x,y)
            if ch in path_chars:
                pways = ways[p] = []
                for d in DIRECTIONS.values():
                    q = p+d
                    qx = int(q.real)
                    qy = int(q.imag)
                    if (0 <= qx < wid and 0 <= qy < hei and lines[qy][qx]!='#'):
                        pways.append(q)
            elif ch!='#':
                direc = DIRECTIONS[ch]
                ways[p] = [p+direc]
    y = hei-1
    x = lines[y].index('.')
    end = complex(x,y)
    x = lines[0].index('.')
    start = complex(x,0)
    return Maze(ways, start, end)

def find_longest(maze, cur, visited, cache):
    key = (cur, visited)
    val = cache.get(key)
    if val is not None:
        return val
    if cur.pos==maze.end:
        cache[key] = val = (0, (maze.end,))
        return val
    if (cur.bit & visited):
        cache[key] = val = (-1, ())
        return val
    vis = visited | cur.bit
    best = -1
    bestjuncs = None
    for nj,path in cur.links.items():
        if (nj.bit & vis):
            continue
        dist,juncs = find_longest(maze, nj, vis, cache)
        if dist >= 0 and dist + len(path) > best:
            best = dist + len(path)
            bestjuncs = (nj,) + juncs
    cache[key] = val = (best, bestjuncs)
    return val

def main():
    lines = sys.stdin.read().strip().splitlines()
    maze = parse_maze(lines, respect_slopes=True)
    maze.find_junctions()
    dist,juncs = find_longest(maze, maze.junctions[0], 0, {})
    print("Part 1:", dist)
    maze = parse_maze(lines, respect_slopes=False)
    maze.find_junctions()
    dist,juncs = find_longest(maze, maze.junctions[0], 0, {})
    print("Part 2:", dist)


if __name__ == '__main__':
    main()
