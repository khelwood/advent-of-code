#!/usr/bin/env python3

import sys

from collections import Counter

def read_sorted_integers():
    return tuple(sorted(map(int, sys.stdin)))

def count_arrangements(current, joltages, target, cache={}):
    key = (current, joltages, target)
    v = cache.get(key)
    if v is not None:
        return v
    count = 0
    if target <= current + 3:
        count += 1
    for i,first in enumerate(joltages):
        if first > current + 3:
            break
        count += count_arrangements(first, joltages[i+1:], target)
    cache[key] = count
    return count

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

    print("Number of arrangements:",
              count_arrangements(0, joltages, joltages[-1]+3))


if __name__ == '__main__':
    main()
