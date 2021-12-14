#!/usr/bin/env python3

import sys
from collections import Counter

def read_data() -> (str, dict):
    lines = sys.stdin.read().strip().splitlines()
    template = lines[0]
    rules = {a.strip():b.strip() for (a,_,b) in
            (line.partition('->') for line in lines if '->' in line)}
    return template, rules

def grow(pairs: dict, rules: dict) -> dict:
    """
    Advance a generation by replacing or keeping a pair's count.
    E.g. if rule is "AB" -> "C"
    then "AB":5 is converted to "AC":5, "CB":5.
    If there is no matching rule, "AB":5 is incorporated in the
    next generation.
    """
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

def freqdiff(pairs: dict, first, last) -> int:
    """
    The difference between the most and least frequent character.
    Because we are counting characters each pair, each
    pair will be counted twice, except for the character
    at the start and the end. So account for them, and
    divide the overall answer by 2.
    """
    counter = Counter((first, last))
    for pair, count in pairs.items():
        a,b = pair
        counter[a] += count
        counter[b] += count
    return (max(counter.values()) - min(counter.values()))//2

def compile_pairs(template: str) -> dict:
    """
    Convert the starting template into a collection of pairs
    of adjacent characters. Track the count of each pair.
    """
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
