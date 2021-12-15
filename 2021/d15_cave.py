#!/usr/bin/env python3

import sys
import bisect

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
    initial_state = (0, (start,), frozenset((start,)))
    states = [initial_state]
    fastest_to = {start:0}
    while states:
        score, path, visited = states.pop(0)
        for nbr in neighbours(path[-1]):
            risk = grid.get(nbr)
            if risk is None or nbr in visited:
                continue
            new_score = score + risk
            f = fastest_to.get(nbr)
            if f is not None and f <= new_score:
                continue
            fastest_to[nbr] = new_score
            new_path = path + (nbr,)
            if nbr==target:
                return (new_path, score+risk)
            state = (new_score, new_path, visited.union((nbr,)))
            bisect.insort_left(states, state)


def main():
    grid, size = read_grid()
    path,risk = least_path(grid, size)
    print("Least risk:", risk)



if __name__ == '__main__':
    main()
