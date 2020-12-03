#!/usr/bin/env python3

import sys

class TreeGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.trees = set()
    def __contains__(self, pos):
        x,y = pos
        x = x%self.width
        return (x,y) in self.trees
    def add_tree(self, pos):
        self.trees.add(pos)

def parse_grid(text, treechar='#'):
    lines = text.splitlines()
    width = len(lines[0])
    height = len(lines)
    grid = TreeGrid(width, height)
    for y,line in enumerate(text.splitlines()):
        for x,ch in enumerate(line):
            if ch==treechar:
                grid.add_tree((x,y))
    return grid

def count_trees(treegrid, start, v):
    x,y = start
    vx,vy = v
    height = treegrid.height
    trees = 0
    while y < height:
        if (x,y) in treegrid:
            trees += 1
        x += vx
        y += vy
    return trees

def main():
    treegrid = parse_grid(sys.stdin.read())
    startpos = (0,0)
    tree_count = count_trees(treegrid, startpos, (3,1))
    print("Initial tree count:", tree_count)

    other_slopes = ((1,1), (5,1), (7,1), (1,2))
    for slope in other_slopes:
        tree_count *= count_trees(treegrid, startpos, slope)
    print("Combined tree count:", tree_count)

if __name__ == '__main__':
    main()
