#!/usr/bin/env python3

import sys
import bisect

class TileGrid:
    def __init__(self, grid, size):
        self.grid = grid
        self.wid, self.hei = size
    def get(self, pos):
        x,y = pos
        if x < 0 or y < 0:
            return None
        hor = x//self.wid
        if hor >= 5:
            return None
        ver = y//self.hei
        if ver >= 5:
            return None
        risk = self.grid[x%self.wid, y%self.hei]
        return (risk + hor + ver + 8)%9 + 1
    @property
    def size(self):
        return (5*self.wid, 5*self.hei)

def neighbours(p):
    x,y = p
    yield (x+1,y)
    yield (x,y+1)
    yield (x-1,y)
    yield (x,y-1)

def read_grid():
    grid = {}
    for y,line in enumerate(sys.stdin.read().strip().splitlines()):
        for x,ch in enumerate(line):
            grid[x,y] = int(ch)
    return grid, (x+1,y+1)

def least_path(grid, size):
    start = (0,0)
    target = (size[0]-1, size[1]-1)
    initial_state = (0, start)
    states = [initial_state]
    fastest_to = {start:0}
    while states:
        score, pos = states.pop(0)
        for nbr in neighbours(pos):
            risk = grid.get(nbr)
            if risk is None:
                continue
            new_score = score + risk
            f = fastest_to.get(nbr)
            if f is not None and f <= new_score:
                continue
            fastest_to[nbr] = new_score
            if nbr==target:
                return new_score
            state = (new_score, nbr)
            bisect.insort_left(states, state)

def main():
    grid, size = read_grid()
    risk = least_path(grid, size)
    print("Small grid least risk:", risk)
    large_grid = TileGrid(grid, size)
    risk = least_path(large_grid, large_grid.size)
    print("Large grid least risk:", risk)

if __name__ == '__main__':
    main()
