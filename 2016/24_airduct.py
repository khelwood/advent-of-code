#!/usr/bin/env python3

import sys
import itertools

sys.path.append('..')

from point import Point
from grid import Grid


def build_maze(lines):
    maze = Grid(len(lines[0]), len(lines), '.')
    targets = {}
    last = 0
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            maze[x,y] = ch
            if ch.isdigit():
                n = int(ch)
                last = max(last, n)
                targets[n] = Point(x,y)
    maze.targets = tuple(targets[i] for i in range(last+1))
    return maze

def find_distances(maze):
    n = len(maze.targets)
    distances = {}
    for si, ei in itertools.combinations(range(n), 2):
        start = maze.targets[si]
        end = maze.targets[ei]
        distance = find_travel_distance(maze, start, end)
        distances[si,ei] = distances[ei,si] = distance
        print('.',end='',flush=True)
    print()
    return distances

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
    x1 = Point(1 if diff.x>1 else -1, 0)
    y1 = Point(0, 1 if diff.y>1 else -1)
    if abs(diff.x) >= abs(diff.y):
        return (x1,y1,-y1,-x1)
    else:
        return (y1,x1,-x1,-y1)

def step_towards_end(maze, pos, end, next_pos, visited):
    for step in directions(pos, end):
        new_pos = pos+step
        if new_pos==end:
            next_pos.append(end)
            visited.add(end)
            return True
        if new_pos not in maze or new_pos in visited or maze[new_pos]=='#':
            continue
        next_pos.append(new_pos)
        visited.add(new_pos)
        if manhattan(new_pos, end)==1:
            break
    return False

def steps_for_permutation(distances, perm, start=0):
    cur = start
    total = 0
    for target in perm:
        steps = distances[cur, target]
        if steps is None:
            return None
        total += steps
        cur = target
    return total

def main():
    maze = build_maze(sys.stdin.read().strip().split('\n'))
    print("Finding distances between targets ", end='', flush=True)
    distances = find_distances(maze)
    best = None
    sequence = range(1, len(maze.targets))
    for perm in itertools.permutations(sequence):
        c = steps_for_permutation(distances, perm)
        if c and (not best or best > c):
            best = c
    print("Steps required:", best)
    # Part 2: end by visiting 0
    best = None
    for perm in itertools.permutations(sequence):
        c = steps_for_permutation(distances, perm+(0,))
        if c and (not best or best > c):
            best = c
    print("Steps required, returning to start:", best)


if __name__ == '__main__':
    main()
