#!/usr/bin/env python3

import sys
from collections import defaultdict

def read_input():
    rules = defaultdict(set)
    seqs = []
    for line in filter(bool, map(str.strip, sys.stdin)):
        if '|' in line:
            a,b = map(int, line.split('|'))
            rules[a].add(b)
        else:
            seqs.append([int(n) for n in line.split(',')])
    return rules, seqs

def invalid_indexes(rules, seq):
    for j,x in enumerate(seq):
        b = rules.get(x)
        if b:
            for i in range(j):
                if seq[i] in b:
                    return i,j
    return None

def correct(rules, seq):
    while (ij := invalid_indexes(rules, seq)):
        i,j = ij
        seq[i],seq[j] = seq[j],seq[i]

def main():
    rules, seqs = read_input()
    total = 0
    invalid = []
    for seq in seqs:
        if invalid_indexes(rules, seq) is None:
            total += seq[len(seq)//2]
        else:
            invalid.append(seq)
    print(total)
    total = 0
    for seq in invalid:
        correct(rules, seq)
        total += seq[len(seq)//2]
    print(total)

if __name__ == '__main__':
    main()
