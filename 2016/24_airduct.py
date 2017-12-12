#!/usr/bin/env python3

import sys
sys.path.append('..')

from point import Point
from grid import Grid
import itertools

DIRECTIONS = (Point(1,0), Point(0,1), Point(-1,0), Point(0,-1))
RIGHT,DOWN,LEFT,UP = DIRECTIONS

def build_maze(lines):
    maze = Grid(len(lines[0]), len(lines), '.')
    targets = [None]*10
    last = 0
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            maze[x,y] = ch
            if ch.isdigit():
                n = int(ch)
                last = max(last, n)
                targets[n] = Point(x,y)
    maze.start = targets[0]
    maze.targets = tuple(targets[1:last+1])
    maze[maze.start] = '.' # Make sure 0 is revisitable
    return maze

def travel(maze, start, end, cache={}):
    """Travel from start to end in the least number of moves."""
    key = (start, end)
    value = cache.get(key)
    if value is None:
        cache[key] = value = find_travel_distance(maze, start, end)
    return value

def find_travel_distance(maze, start, end):
    if start==end:
        return 0
    visited = {start}
    next_pos = [start]
    moves = 0
    success = (start==end)
    while next_pos:
        moves += 1
        cur_pos = next_pos
        next_pos = []
        for pos in cur_pos:
            if step_towards_end(maze, pos, end, next_pos, visited):
                return moves
    return None

def manhattan(p1, p2):
    return (abs(p1[0]-p2[0])+abs(p1[1]-p2[1]))

def directions(pos, end):
    diff = end-pos
    if abs(diff.x)+abs(diff.y)==1:
        return (diff,)
    x1,x2 = (RIGHT,LEFT) if diff.x>1 else (LEFT,RIGHT)
    y1,y2 = (DOWN,UP) if diff.y>1 else (UP,DOWN)
    if abs(diff.x) >= abs(diff.y):
        return (x1,y1,y2,x2)
    else:
        return (y1,x1,x2,y2)

def step_towards_end(maze, pos, end, next_pos, visited):
    for step in directions(pos, end):
        new_pos = pos+step
        if new_pos==end:
            next_pos.append(end)
            visited.add(end)
            return True
        if new_pos not in maze or new_pos in visited or maze[new_pos]!='.':
            continue
        next_pos.append(new_pos)
        visited.add(new_pos)
        if manhattan(new_pos, end)==1:
            break
    return False

def steps_for_permutation(maze, start, perm):
    #print("Trying", perm)
    cur = start
    total = 0
    for target in perm:
        #print("Travelling to", target)
        steps = travel(maze, cur, target)
        if steps is None:
            return None
        total += steps
        cur = target
    return total

def main():
    maze = build_maze(sys.stdin.read().strip().split('\n'))
    print(maze.targets)
    best = None
    for perm in itertools.permutations(maze.targets):
        c = steps_for_permutation(maze, maze.start, perm)
        if c and (not best or best > c):
            best = c
    print("Steps required:", best)
    # Part 2: end by visiting 0
    best = None
    for perm in itertools.permutations(maze.targets):
        c = steps_for_permutation(maze, maze.start, perm+(maze.start,))
        if c and (not best or best > c):
            best = c
    print("Steps required, returning to start:", best)


if __name__ == '__main__':
    main()
