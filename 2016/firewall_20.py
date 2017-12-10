#!/usr/bin/env python3

import sys
from collections import namedtuple

BlockRange = namedtuple('BlockRange', 'start end')

def makeblockrange(line):
    i = line.index('-')
    return BlockRange(int(line[:i]), int(line[i+1:]))

def find_least_unblocked(ranges):
    num = 0
    for r in ranges:
        if r.start > num:
            return num
        num = max(num, r.end+1)
    return num

def count_unblocked(ranges):
    count = 0
    top = 0
    for r in ranges:
        if r.start > top:
            count += r.start - top
        top = max(top, r.end+1)
    max_value = (1<<32)-1
    if max_value > top:
        count += max_value - top
    return count

def main():
    data = sys.stdin.read().strip()
    ranges = [makeblockrange(line) for line in data.split('\n')]
    ranges.sort() # sorts by start
    x = find_least_unblocked(ranges)
    print("Least unblocked:", x)
    n = count_unblocked(ranges)
    print("Num unblocked:", n)

if __name__ == '__main__':
    main()
