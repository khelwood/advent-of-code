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

def expand_lan(lan, links):
    expanded = False
    a = next(iter(lan))
    for b in links[a]:
        if b not in lan and lan <= links[b]:
            if not expanded:
                expanded = True
                lan = set(lan)
            lan.add(b)
    if expanded:
        return frozenset(lan)
    return None

def find_largest_lan(links):
    lans = find_trios(links)
    all_lans = set()
    new_lans = lans
    while new_lans:
        all_lans |= new_lans
        cur_lans = new_lans
        new_lans = set()
        for lan in cur_lans:
            lan = expand_lan(lan, links)
            if lan:
                new_lans.add(lan)
    return max(all_lans, key=len)

def main():
    links = read_links()
    trios = find_trios(links, lambda a:a.startswith('t'))
    print(len(trios))
    lan = find_largest_lan(links)
    print(','.join(sorted(lan)))

if __name__ == '__main__':
    main()
