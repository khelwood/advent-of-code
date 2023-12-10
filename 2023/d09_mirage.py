#!/usr/bin/env python3

import sys

def parse_seq(line):
    return list(map(int, line.split()))

def build_layers(seq):
    seqs = [seq]
    while any(seq):
        seq = find_diffs(seq)
        if seq:
            seqs.append(seq)
    return seqs

def find_diffs(seq):
    diffs = []
    it = iter(seq)
    last = next(it)
    for n in it:
        diffs.append(n-last)
        last = n
    return diffs

def extrapolate(cake):
    d = 0
    for layer in reversed(cake):
        d += layer[-1]
        layer.append(d)

def extrapolate_left(cake):
    d = 0
    for layer in reversed(cake):
        d = layer[0] - d
        layer.insert(0, d)

def main():
    seqs = [parse_seq(line) for line in sys.stdin.read().strip().splitlines()]
    xp_functions = (extrapolate, extrapolate_left)
    indexes = [-1, 0]
    for i in range(2):
        xp = xp_functions[i]
        index = indexes[i]
        cakes = list(map(build_layers, seqs))
        total = 0
        for layers in cakes:
            xp(layers)
            total += layers[0][index]
        print(f"Part {i+1}: {total}")

if __name__ == '__main__':
    main()
