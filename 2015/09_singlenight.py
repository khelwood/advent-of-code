#!/usr/bin/env python3

import sys
import re
import itertools

def parse_distances(lines, ptn=re.compile(r'^(\w+) to (\w+) = ([0-9]+)$')):
    distances = {}
    cities = set()
    for line in lines:
        m = ptn.match(line)
        if not m:
            raise ValueError(repr(line))
        a,b = [m.group(i) for i in (1,2)]
        distance = int(m.group(3))
        cities.add(a)
        cities.add(b)
        distances[a,b] = distance
        distances[b,a] = distance
    return cities, distances

def total_distance(seq, distances):
    return sum(distances[seq[i], seq[i+1]] for i in range(len(seq)-1))

def find_shortest_distance(cities, distances):
    return min(total_distance(perm, distances)
                   for perm in itertools.permutations(cities))

def find_longest_distance(cities, distances):
    return max(total_distance(perm, distances)
                   for perm in itertools.permutations(cities))

def main():
    lines = sys.stdin.read().strip().split('\n')
    cities, distance = parse_distances(lines)
    shortest = find_shortest_distance(cities, distance)
    print("Shortest distance:", shortest)
    longest = find_longest_distance(cities, distance)
    print("Longest distance:", longest)


if __name__ == '__main__':
    main()
