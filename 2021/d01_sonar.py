#!/usr/bin/env python3

import sys

def count_up(seq):
    n = 0
    it = iter(seq)
    last = next(it)
    for cur in it:
        if cur > last:
            n += 1
        last = cur
    return n

def sliding_sum(seq, n):
    ln = len(seq)
    total = sum(seq[i] for i in range(0, n))
    yield total
    for i in range(n, ln):
        total += seq[i] - seq[i-n]
        yield total

def main():
    numbers = list(map(int, sys.stdin.read().strip().splitlines()))
    print("Upticks:", count_up(numbers))
    print("Sliding sum upticks:", count_up(sliding_sum(numbers, 3)))

if __name__ == '__main__':
    main()
