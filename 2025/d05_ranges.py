#!/usr/bin/env python3

import sys

def read_input():
    ranges = []
    ids = []
    for line in filter(bool, map(str.strip, sys.stdin)):
        if '-' in line:
            a,_,b = line.partition('-')
            ranges.append((int(a),int(b)))
        else:
            ids.append(int(line))
    return ranges, ids

def merge_ranges(ranges):
    ranges.sort()
    output = []
    la = lb = None
    for a,b in ranges:
        if la is None:
            la,lb = a,b
            continue
        if a <= lb+1:
            lb = max(lb,b)
        else:
            output.append((la,lb))
            la,lb = a,b
    output.append((la,lb))
    return output

def in_ranges(ranges, i):
    return any(a <= i <= b for (a,b) in ranges)

def main():
    ranges, ids = read_input()
    ranges = merge_ranges(ranges)
    print(sum(in_ranges(ranges, i) for i in ids))
    print(sum(b+1-a for (a,b) in ranges))

if __name__ == '__main__':
    main()
