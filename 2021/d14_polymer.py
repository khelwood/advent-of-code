#!/usr/bin/env python3

import sys
from collections import Counter

def read_data():
    lines = sys.stdin.read().strip().splitlines()
    template = lines[0]
    rules = {a.strip():b.strip() for (a,_,b) in
            (line.partition('->') for line in lines if '->' in line)}
    return template, rules

def grow(pairs, rules):
    new_pairs = Counter()
    for pair, count in pairs.items():
        value = rules.get(pair)
        if value:
            a,b = pair
            new_pairs[a+value] += count
            new_pairs[value+b] += count
        else:
            new_pairs[pair] += count
    return new_pairs


def freqdiff(pairs, first, last):
    counter = Counter()
    for pair, count in pairs.items():
        a,b = pair
        counter[a] += count
        counter[b] += count
    counter[first] += 1
    counter[last] += 1
    return (max(counter.values()) - min(counter.values()))//2

def compile_pairs(template):
    pairs = Counter()
    for i in range(len(template)-1):
        pair = template[i] + template[i+1]
        pairs[pair] += 1
    return pairs

def main():
    template, rules = read_data()
    first = template[0]
    last = template[-1]
    pairs = compile_pairs(template)
    for _ in range(10):
        pairs = grow(pairs, rules)
    print("After 10: most-least:", freqdiff(pairs, first, last))
    for _ in range(10,40):
        pairs = grow(pairs, rules)
    print("After 40: most-least:", freqdiff(pairs, first, last))

if __name__ == '__main__':
    main()
