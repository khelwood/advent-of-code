#!/usr/bin/env python3

import sys
import itertools

def checksum(row):
    return max(row)-min(row)

def divisor_sum(row):
    for (a,b) in itertools.combinations(row, 2):
        if a < b:
            if b%a==0:
                return b//a
        else:
            if a%b==0:
                return a//b

def main():
    lines = sys.stdin.read().strip().split('\n')
    data = [[int(n) for n in line.split()] for line in lines]
    cs = sum(map(checksum, data))
    print("Checksum:", cs)
    ds = sum(map(divisor_sum, data))
    print("Division sum:", ds)

if __name__ == '__main__':
    main()
