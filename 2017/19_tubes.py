#!/usr/bin/env python3

import sys

sys.path.append('..')
from point import Point
from grid import Grid

def construct_maze(lines):
    maze = Grid(len(lines[0]), len(lines), ' ')
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            maze[x,y] = ch
    return maze

def can_advance(maze, pos, direc):
    np = pos + direc
    if np not in maze:
        return False
    v1 = maze[np]
    if v1==' ':
        return False
    v0 = maze[pos]
    if v0!='+':
        return True # assume we always end at an indicated junction
    return (v1==('-' if direc.x else '|'))

def can_turn(maze, pos, direc):
    np = pos + direc
    if np not in maze:
        return False
    v1 = maze[np]
    return v1==('-' if direc.x else '|')
    # In my input, there is never a letter directly after
    # a turn. If there was, navigation would be more ambiguous;
    # but as it is, it is easy to tell where we can turn.

def turn_left(direc):
    return Point(direc[1], -direc[0])

def turn_right(direc):
    return Point(-direc[1], direc[0])

def new_direction(maze, pos, direc):
    if maze[pos]=='+':
        left = turn_left(direc)
        if can_turn(maze, pos, left):
            return left
        right = turn_right(direc)
        if can_turn(maze, pos, right):
            return right
    return None

def traverse(maze):
    startx = next(x for x in range(maze.width) if maze[x,0]=='|')
    position = Point(startx, 0)
    direction = Point(0, 1)
    letters = []
    steps = 1
    while True:
        if not can_advance(maze, position, direction):
            new_direc = new_direction(maze, position, direction)
            if new_direc is None:
                break
            direction = new_direc
        position += direction
        steps += 1
        ch = maze[position]
        if 'A'<=ch<='Z':
            letters.append(ch)
    return steps, letters


def main():
    lines = sys.stdin.read().split('\n')
    maze = construct_maze(lines)
    steps, sequence = traverse(maze)
    print(''.join(sequence))
    print(steps)

if __name__ == '__main__':
    main()
