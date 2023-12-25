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
                d,nj = self.next_junction(junc.pos, q)
                if d >= 0:
                    nj = pos_junction[nj]
                    junc.links[nj] = d

    def next_junction(self, start, cur):
        dist = 1
        last = start
        while True:
            ways = self.ways[cur]
            if len(ways) > 2 or cur==self.end:
                return dist,cur
            p = next((pp for pp in ways if pp!=last), None)
            if p is None:
                return -1,None
            last = cur
            cur = p
            dist +=1

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
    n = cache.get(key)
    if n is not None:
        return n
    if cur.pos==maze.end:
        cache[key] = 0
        return 0
    if (cur.bit & visited):
        cache[key] = -1
        return -1
    vis = visited | cur.bit
    best = -1
    for nx,d in cur.links.items():
        if (nx.bit & vis):
            continue
        newd = find_longest(maze, nx, vis, cache) + d
        if newd > best:
            best = newd
    cache[key] = best
    return best

def main():
    lines = sys.stdin.read().strip().splitlines()
    maze = parse_maze(lines, respect_slopes=True)
    maze.find_junctions()
    dist = find_longest(maze, maze.junctions[0], 0, {})
    print("Part 1:", dist)
    maze = parse_maze(lines, respect_slopes=False)
    maze.find_junctions()
    dist = find_longest(maze, maze.junctions[0], 0, {})
    print("Part 2:", dist)


if __name__ == '__main__':
    main()
