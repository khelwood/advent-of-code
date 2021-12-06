#!/usr/bin/env python3

import sys

def advance_counts(counts):
    newcounts = {}
    for i in range(8):
        newcounts[i] = counts[i+1]
    newcounts[8] = counts[0]
    newcounts[6] += counts[0]
    return newcounts

def main():
    initial = tuple(map(int, sys.stdin.read().replace(',', ' ').split()))
    counts = {n:0 for n in range(9)}
    for n in initial:
        counts[n] += 1
    for _ in range(80):
        counts = advance_counts(counts)
    print("Total after 80 days: ", sum(counts.values()))
    for _ in range(80, 256):
        counts = advance_counts(counts)
    print("Total after 256 days: ", sum(counts.values()))

if __name__ == '__main__':
    main()
