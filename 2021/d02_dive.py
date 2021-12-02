#!/usr/bin/env python3

import sys

def read_moves(lines):
    for line in lines:
        w,n = line.split()
        yield (w, int(n))

def follow_moves(moves):
    x = y = 0
    for w, n in moves:
        if w=='forward':
            x += n
        elif w=='up':
            y -= n
        elif w=='down':
            y += n
    return x,y

def follow_aim(moves):
    x = y = aim = 0
    for w,n in moves:
        if w=='down':
            aim += n
        elif w=='up':
            aim -= n
        elif w=='forward':
            x += n
            y += aim * n
    return x,y

def main():
    moves = list(read_moves(sys.stdin.read().splitlines()))
    x,y = follow_moves(moves)
    print("Without aim:")
    print(f"Horizontal: {x}, Vertical: {y}")
    print("Product:", x*y)
    x,y = follow_aim(moves)
    print("With aim:")
    print(f"Horizontal: {x}, Vertical: {y}")
    print("Product:", x*y)

if __name__ == '__main__':
    main()
