#!/usr/bin/env python3

import sys

def find_best_target_moves(values, left, right, dist_func=abs):
    best_target = None
    best_moves = None
    for target in range(left, right+1):
        moves = sum(dist_func(target-n) for n in values)
        if best_moves is None or moves < best_moves:
            best_moves = moves
            best_target = target
    return best_target, best_moves

def fuel(n):
    n = abs(n)
    return n * (n+1)//2

def main():
    initial = tuple(map(int, sys.stdin.read().strip().replace(',',' ').split()))
    left = min(initial)
    right = max(initial)

    target, moves = find_best_target_moves(initial, left, right)
    print("First target position:", target)
    print("Moves required:", moves)
    target, fuel_needed = find_best_target_moves(initial, left, right, fuel)
    print("Second target position:", target)
    print("Fuel required:", fuel_needed)

if __name__ == '__main__':
    main()
