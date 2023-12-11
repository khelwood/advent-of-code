#!/usr/bin/env python3

import sys

from itertools import combinations

class Space:
    def __init__(self, lines):
        self.lines = lines
        galaxies = []
        for y,line in enumerate(lines):
            for x,ch in enumerate(line):
                if ch=='#':
                    galaxies.append((x,y))
        self.galaxies = galaxies
        fixed_columns = set()
        fixed_rows = set()
        for (x,y) in galaxies:
            fixed_rows.add(y)
            fixed_columns.add(x)
        self.expanded_columns = set(range(self.wid)) - fixed_columns
        self.expanded_rows = set(range(self.hei)) - fixed_rows

    @property
    def wid(self):
        return len(self.lines[0])

    @property
    def hei(self):
        return len(self.lines)

    def update_galaxies(self, distance):
        col_map = []
        diff = 0
        for x in range(self.wid):
            if x in self.expanded_columns:
                diff += distance
            col_map.append(x + diff)
        row_map = []
        diff = 0
        for y in range(self.hei):
            if y in self.expanded_rows:
                diff += distance
            row_map.append(y + diff)
        return [(col_map[x], row_map[y]) for (x,y) in self.galaxies]


def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def main():
    space = Space(sys.stdin.read().strip().splitlines())
    galaxies = space.update_galaxies(1)
    distance = sum(manhattan(a,b) for (a,b) in combinations(galaxies, 2))
    print("Part 1:", distance)
    galaxies = space.update_galaxies(999_999)
    distance = sum(manhattan(a,b) for (a,b) in combinations(galaxies, 2))
    print("Part 2:", distance)


if __name__ == '__main__':
    main()
