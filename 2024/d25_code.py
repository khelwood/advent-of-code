#!/usr/bin/env python3

import sys

def read_schematics():
    keys = []
    locks = []
    text = sys.stdin.read().strip()
    blocks = text.split('\n\n')
    for block in blocks:
        lines = block.splitlines()
        heights = tuple(sum(line[j]=='#' for line in lines)-1 for j in range(5))
        group = locks if lines[0][0]=='#' else keys
        group.append(heights)
    return keys,locks

def matches(key, lock):
    return all(a+b <= 5 for (a,b) in zip(key,lock))

def main():
    keys,locks = read_schematics()
    total = 0
    for key in keys:
        for lock in locks:
            if matches(key,lock):
                total += 1
    print(total)


if __name__ == '__main__':
    main()
