#!/usr/bin/env python3

import sys

from typing import NamedTuple

class Row(NamedTuple):
    line: str
    groups: tuple

def parse_row(text):
    i = text.index(' ')
    line = text[:i]
    groups = tuple(map(int, text[i+1:].split(',')))
    return Row(line, groups)

def cache(func):
    cache = {}
    def wrapper(string, groups):
        key = (string, groups)
        v = cache.get(key)
        if v is None:
            v = cache[key] = func(string, groups)
        return v
    return wrapper

@cache
def count_ways(string, groups):
    min_len = sum(groups) + len(groups)-1
    if len(string) < min_len:
        return 0
    i = string.find('#')
    j = string.find('?')
    if not groups:
        return int(i < 0)
    if i < 0 and j < 0:
        return 0
    g = groups[0]
    ls = len(string)
    if i < 0 or 0 <= j < i:
        i = j
    if ls < i+min_len:
        return 0
    n = 0
    if all(string[h] in '?#' for h in range(i+1, i+g)):
        if ls==i+g:
            return int(len(groups)==1)
        if string[i+g] in '?.':
            n = count_ways(string[i+g+1:], groups[1:])
    if j==i: # spring here was optional
        n += count_ways(string[i+1:], groups)
    return n

def expand(row):
    line = '?'.join(5*[row.line])
    return Row(line, 5*row.groups)

def main():
    rows = list(map(parse_row, sys.stdin.read().strip().splitlines()))
    total = sum(count_ways(row.line, row.groups) for row in rows)
    print("Part 1:", total)
    total = sum(count_ways(row.line, row.groups) for row in map(expand, rows))
    print("Part 2:", total)

if __name__ == '__main__':
    main()
