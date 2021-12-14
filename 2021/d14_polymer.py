#!/usr/bin/env python3

import sys
from collections import Counter

def read_data():
    lines = sys.stdin.read().strip().splitlines()
    template = lines[0]
    rules = {a.strip():b.strip() for (a,_,b) in
            (line.partition('->') for line in lines if '->' in line)}
    return template, rules

def grow(polymer, rules):
    i = 1
    while i < len(polymer):
        key = polymer[i-1] + polymer[i]
        value = rules.get(key)
        if value:
            polymer.insert(i, value)
            i += 1
        i += 1

def freqdiff(polymer):
    counter = Counter(polymer)
    most = max(counter.values())
    least = min(counter.values())
    return most-least

def main():
    template, rules = read_data()
    polymer = list(template)
    for _ in range(10):
        grow(polymer, rules)
    print("After 10: most-least:", freqdiff(polymer))
    for i in range(10,40):
        print(i,end='\r',flush=True)
        grow(polymer, rules)
    print("After 40: most-least:", freqdiff(polymer))


if __name__ == '__main__':
    main()
