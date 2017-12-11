#!/usr/bin/env python3

import sys
import re
import itertools
sys.path.append('..')

from point import Point
from grid import Grid

NODE_PTN = re.compile(r'/dev/grid/(node-x([0-9]+)-y([0-9]+)) #T #T #T '
                .replace(' ',r'\s+').replace('#', '([0-9]+)'))

class Node:
    def __init__(self, desc, pos, size, used, avail):
        self.desc = desc
        self.position = pos
        self.size = size
        self.used = used
        self.avail = avail
    def __str__(self):
        return self.desc
    def __repr__(self):
        return 'Node(%r, %r, %r, %r, %r)'%(
            self.desc, self.position, self.size, self.used, self.avail)

def make_node(text):
    m = NODE_PTN.match(text)
    if not m:
        return None
    desc = m.group(1)
    x = int(m.group(2))
    y = int(m.group(3))
    size = int(m.group(4))
    used = int(m.group(5))
    avail = int(m.group(6))
    return Node(desc, Point(x,y), size, used, avail)

def count_viable_pairs(nodes):
    count = 0
    for a,b in itertools.combinations(nodes, 2):
        if 0 < a.used <= b.avail:
            count += 1
        if 0 < b.used <= a.avail:
            count += 1
    return count
    
def main():
    nodes = list(x for x in map(make_node, sys.stdin) if x is not None)
    vp = count_viable_pairs(nodes)
    print("Viable pairs:", vp)
    m = Point.max(*(n.position for n in nodes))
    grid = Grid(m.x+1, m.y+1)
    for node in nodes:
        grid[node.position] = node
    source = grid[grid.width-1, 0]
    print("Source is", source)
    dest = grid[0,0]
    print("Destination is", dest)


if __name__ == '__main__':
    main()
