#!/usr/bin/env python3

import sys
import re
import itertools

from collections import defaultdict

HAPPY_PTN = re.compile('^% would (lose|gain) # happiness units? by '
                        'sitting next to %.$'
                        .replace('%', r'([\w+]+)').replace('#', '([0-9]+)'))

def pair_key(x,y):
    return (x,y) if x<=y else (y,x)

def parse_relationships(lines):
    names = set()
    relationships = defaultdict(int)
    for line in lines:
        m = re.match(HAPPY_PTN, line)
        if not m:
            raise ValueError(repr(line))
        name1 = m.group(1)
        sign = 1 if m.group(2)=='gain' else -1
        name2 = m.group(4)
        relationships[pair_key(name1, name2)] += sign*int(m.group(3))
        names.add(name1)
        names.add(name2)
    return list(names), relationships

def score_arrangement(first_name, others, relationships):
    score = 0
    prev = first_name
    for name in others:
        score += relationships[pair_key(prev, name)]
        prev = name
    score += relationships[pair_key(prev, first_name)]
    return score

def best_score(names, relationships):
    first_name = names[0]
    return max(score_arrangement(first_name, others, relationships)
                for others in itertools.permutations(names[1:]))

def main():
    lines = sys.stdin.read().strip().split('\n')
    names, relationships = parse_relationships(lines)
    score = best_score(names, relationships)
    print("Best score:", score)
    score = best_score(names+['me'], relationships)
    print("Best score including me:", score)
    
if __name__ == '__main__':
    main()
