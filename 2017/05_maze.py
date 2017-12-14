#!/usr/bin/env python3

import sys

def follow_jumps(numbers, altered):
    numbers = numbers[:]
    pos = 0
    count = 0
    n = len(numbers)
    while 0 <= pos < n:
        count += 1
        value = numbers[pos]
        numbers[pos] += (-1 if altered and value >= 3 else 1)
        pos += value
    return count

def main():
    numbers = [int(n) for n in sys.stdin.read().split()]
    print(" working...", end='\r')
    steps = follow_jumps(numbers, False)
    print("Part 1 steps:", steps)
    print(" working...", end='\r')
    steps = follow_jumps(numbers, True)
    print("Part 2 steps:", steps)

if __name__ == '__main__':
    main()
