#!/usr/bin/env python3

import sys

from collections import Counter

def read_sorted_integers():
    return tuple(sorted(map(int, sys.stdin)))

def count_arrangements(joltages):
    n = len(joltages)
    counts = [0] * n
    counts[-1] = 1
    for i in range(n-2, -1, -1):
        boundary = joltages[i] + 3
        c = 0
        for j in range(i+1, n):
            if joltages[j] > boundary:
                break
            c += counts[j]
        counts[i] = c
    boundary = 3
    c = 0
    for j in range(n):
        if joltages[j] > boundary:
            break
        c += counts[j]
    return c

def main():
    joltages = read_sorted_integers()
    jumps = Counter()
    joltage = 0
    for v in joltages:
        if v > joltage + 3:
            raise ValueError(f"Joltage jump too high: {joltage} -> {v}")
        jumps[v-joltage] += 1
        joltage = v
    jumps[3] += 1 # device joltage = highest + 3
    print(jumps)
    print("(1 jolt jumps) * (3 jolt jumps) =", jumps[1]*jumps[3])
    print("Number of arrangements:", count_arrangements(joltages))

if __name__ == '__main__':
    main()
