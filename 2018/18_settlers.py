#!/usr/bin/env python3

import sys
import itertools

OPEN = '.'
TREE = '|'
YARD = '#'

ADJACENT = ((-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1))

class Area:
    def __init__(self, lines):
        self.trees = set()
        self.yards = set()
        for y,line in enumerate(lines):
            for x,value in enumerate(line.strip()):
                if value==YARD:
                    self.yards.add((x,y))
                elif value==TREE:
                    self.trees.add((x,y))
        self.width = x+1
        self.height = y+1
    def __getitem__(self, pos):
        if pos in self.trees:
            return TREE
        if pos in self.yards:
            return YARD
        return OPEN
    def __setitem__(self, pos, value):
        if value==TREE:
            self.yards.discard(pos)
            self.trees.add(pos)
        elif value==YARD:
            self.trees.discard(pos)
            self.yards.add(pos)
        else:
            self.trees.discard(pos)
            self.yards.discard(pos)
    @property
    def num_trees(self):
        return len(self.trees)
    @property
    def num_yards(self):
        return len(self.yards)
    def count_adjacent_trees(self, pos, dirs=ADJACENT):
        return sum((addp(pos, d) in self.trees) for d in dirs)
    def count_adjacent_yards(self, pos, dirs=ADJACENT):
        return sum((addp(pos, d) in self.yards) for d in dirs)
    def advance(self):
        removed_yards = []
        new_yards = []
        new_trees = []
        trees = self.trees
        yards = self.yards
        for pos in itertools.product(range(self.width), range(self.height)):
            if pos in trees:
                if self.count_adjacent_yards(pos)>=3:
                    new_yards.append(pos)
            elif pos in yards:
                if (self.count_adjacent_yards(pos)==0
                        or self.count_adjacent_trees(pos)==0):
                    removed_yards.append(pos)
            else:
                if self.count_adjacent_trees(pos)>=3:
                    new_trees.append(pos)
        yards.difference_update(removed_yards)
        trees.difference_update(new_yards)
        yards.update(new_yards)
        trees.update(new_trees)
    def display(self):
        for y in range(self.height):
            print(''.join([self[x,y] for x in range(self.width)]))

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def main():
    area = Area(sys.stdin)
    for _ in range(10):
        area.advance()
    print("Resource value after 10 minutes:", area.num_trees*area.num_yards)

if __name__ == '__main__':
    main()
