#!/usr/bin/env python3

import sys

def find_connections(lines):
    connections = {}
    for line in lines:
        left, rights = line.split(' <-> ')
        left = int(left.strip())
        rights = {int(r.strip()) for r in rights.replace(',',' ').split()}
        connections[left] = rights
    return connections

def find_group(connections, start):
    found = set()
    new = {start}
    while new:
        found |= new
        prev = new
        new = set()
        for i in prev:
            new |= connections[i]
        new -= found
    return found

def find_all_groups(connections):
    all_keys = set(connections)
    groups = []
    while all_keys:
        n = next(iter(all_keys))
        g = find_group(connections, n)
        all_keys -= g
        groups.append(g)
    return groups

def main():
    lines = sys.stdin.read().strip().split('\n')
    connections = find_connections(lines)
    group_zero = find_group(connections, 0)
    print("Number in group zero:", len(group_zero))
    groups = find_all_groups(connections)
    print("Number of groups:", len(groups))

if __name__ == '__main__':
    main()
