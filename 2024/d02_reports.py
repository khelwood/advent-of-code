#!/usr/bin/env python3

import sys

def read_seqs():
    return [list(map(int, line.split()))
       for line in sys.stdin.read().strip().splitlines()]

def pair_iter(seq):
    it = iter(seq)
    prev = next(it)
    for x in it:
        yield (prev,x)
        prev = x

def pt_direc(a,b):
    return 1 if b > a else -1 if b < a else 0

def find_direction(seq):
    counts = {-1:0, 1:0}
    for a,b in pair_iter(seq):
        d = pt_direc(a,b)
        if d!=0:
            counts[d] += 1
    return max(counts, key=counts.get)

def find_unsafe(seq, direc):
    for i,(a,b) in enumerate(pair_iter(seq)):
        d = pt_direc(a,b)
        if d != direc:
            return i
        if abs(b-a) > 3:
            return i
    return -1

def safe(seq):
    return find_unsafe(seq, find_direction(seq)) < 0

def tolerable(seq):
    direc = find_direction(seq)
    i = find_unsafe(seq, direc)
    if i < 0:
        return True
    return (find_unsafe(seq[:i]+seq[i+1:], direc) < 0
         or find_unsafe(seq[:i+1]+seq[i+2:], direc) < 0)

def main():
    seqs = read_seqs()
    print(sum(map(safe, seqs)))
    print(sum(map(tolerable, seqs)))

if __name__ == '__main__':
    main()
