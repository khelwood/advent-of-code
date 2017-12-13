#!/usr/bin/env python3

import sys
sys.path.append('..')

from point import Point

DEST = Point(31,39)
START = Point(1,1)

UP = Point(0,-1)
DOWN = Point(0,1)
LEFT = Point(1,0)
RIGHT = Point(-1,0)
DIRECTIONS = (RIGHT, DOWN, LEFT, UP)

def is_open(p, cache={}):
    p = Point.of(p)
    v = cache.get(p)
    if v is not None:
        return v
    v = calc_open(p)
    cache[p] = v
    return v

def calc_open(p):
    x,y = p
    if x<0 or y<0:
        return False
    n = x*x + 3*x + 2*x*y + y + y*y + MAZE_SEED
    return (count_bits(n)&1)==0

def count_bits(n):
    return bin(n).count('1')

def str_pos(p, seen):
    if not is_open(p):
        return '#'
    if seen and p in seen:
        return 'O'
    return '.'

def draw_maze(w,h, seen=None):
    for y in range(h):
        print(' '.join(str_pos((x,y), seen) for x in range(w)))

def directions(d):
    """Directions, biased towards the destination"""
    if d.x >= 0:
        x1 = RIGHT
        x2 = LEFT
    else:
        x1 = LEFT
        x2 = RIGHT
    if d.y >= 0:
        y1 = DOWN
        y2 = UP
    else:
        y1 = UP
        y2 = DOWN
    if abs(d.x) >= abs(d.y):
        return (x1, y1, y2, x2)
    return (y1, x1, x2, y2)
        
def find_end(current_pos, next_pos, seen):
    for p in current_pos:
        for d in directions(DEST-p):
            n = p+d
            if n==DEST:
                return True
            if is_open(n) and n not in seen:
                next_pos.append(n)
                seen.add(n)
    return False

def find_next_moves(current_pos, next_pos, seen):
    for p in current_pos:
        for d in DIRECTIONS:
            n = p+d
            if is_open(n) and n not in seen:
                next_pos.append(n)
                seen.add(n)
        
def main():
    global MAZE_SEED
    if len(sys.argv)<=1:
        exit("Usage: %s <maze-seed>"%sys.argv[0])
    MAZE_SEED = int(sys.argv[1])
    moves = 1
    seen = {START}
    current_pos = [START]
    next_pos = []
    while not find_end(current_pos, next_pos, seen):
        moves += 1
        print(f' (Moves: {moves}, visited: {len(seen)})   ', end='\r')
        current_pos = next_pos
        next_pos = []
    print(f'Steps to target: {moves}'.ljust(70))
    max_moves = 50
    moves = 0
    seen = {START}
    current_pos = [START]
    next_pos = []
    while moves < max_moves:
        moves += 1
        find_next_moves(current_pos, next_pos, seen)
        current_pos = next_pos
        next_pos = []
    print(f"Places within {max_moves} steps: {len(seen)}\n")
    m = Point.max(seen)
    draw_maze(m.x+2,m.y+2,seen)

if __name__ == '__main__':
    main()
