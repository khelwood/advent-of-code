#!/usr/bin/env python3

import sys

from collections import defaultdict
from itertools import combinations

def read_links():
    links = defaultdict(set)
    for line in filter(bool, map(str.strip, sys.stdin)):
        a,b = line.split('-')
        links[a].add(b)
        links[b].add(a)
    return links

def find_trios(links, pred=None):
    trios = set()
    for a,bs in links.items():
        if pred is None or pred(a):
            for b1,b2 in combinations(bs, 2):
                if b2 in links[b1]:
                    trios.add(frozenset((a,b1,b2)))
    return trios

def expand_lans(lans, links):
    expanded = set()
    for lan in lans:
        a = next(iter(lan))
        for b in links[a]:
            bl = links[b]
            if b not in lan and all(x==b or x in bl for x in lan):
                expanded.add(lan|{b})
    return expanded

def find_largest_lans(links):
    new_lans = find_trios(links)
    while new_lans:
        lans = new_lans
        new_lans = expand_lans(lans, links)
    return lans

def main():
    links = read_links()
    trios = find_trios(links, lambda a:a.startswith('t'))
    print(len(trios))
    lans = find_largest_lans(links)
    assert len(lans)==1
    lan, = lans
    print(','.join(sorted(lan)))

if __name__ == '__main__':
    main()
