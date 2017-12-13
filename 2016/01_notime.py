#!/usr/bin/env python3

import sys

sys.path.append('..')

from point import Point

def manhattan(p):
    return abs(p.x)+abs(p.y)

def main():
    instructions = sys.stdin.read().replace(',',' ').split()
    direction = Point(0,1) # North
    position = Point(0,0)
    visited = { position }
    visited_twice = None
    for step in instructions:
        if step.startswith('L'):
            direction = Point(-direction.y, direction.x)
        else:
            direction = Point(direction.y, -direction.x)
        n = int(step[1:])
        for _ in range(n):
            position += direction
            if visited_twice is None:
                if position in visited:
                    visited_twice = position
                else:
                    visited.add(position)
    print("Final position:", position, "at distance:", manhattan(position))
    print("First repeated position:", visited_twice,
              "at distance:", manhattan(visited_twice))

if __name__ == '__main__':
    main()
