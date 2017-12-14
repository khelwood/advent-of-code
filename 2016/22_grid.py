#!/usr/bin/env python3

"""Observations:
Most of the nodes are around 90T in size.
A few are much bigger, around 500T.
The big ones all contain too much date to be moved: they are
essentially obstacles.
Of the normal size ones, one is empty, and the rest contain
about 70T. Therefore no node can contain two nodes' worth of data.
Essentially, this is a slide puzzle. There is always one empty slot,
and that one is always the destination for the next move.
"""

import sys
import re
import itertools
from collections import namedtuple

sys.path.append('..')
from point import Point

LEFT = Point(-1,0)
RIGHT = Point(1,0)
DOWN = Point(0,1)
UP = Point(0,-1)

PRIZE, DESTINATION, OBSTACLE, EMPTY, NORMAL = '*X#O.'

NODE_PTN = re.compile(r'/dev/grid/node-x#-y# #T #T #T '
                .replace(' ',r'\s+').replace('#', '([0-9]+)'))

Node = namedtuple('Node', 'position size used avail')
    
def make_node(text):
    m = NODE_PTN.match(text)
    if not m:
        return None
    args = [int(m.group(i+1)) for i in range(5)]
    args[0:2] = [Point(args[0], args[1])]
    return Node(*args)
    
class State:
    def __init__(self, width, height, prize, dest, empty, obstacles):
        self.width = width
        self.height = height
        self.prize = prize
        self.dest = dest
        self.empty = empty
        self.obstacles = obstacles
        self.moves = 0
    def find_route(self):
        while self.prize != self.dest:
            if self.prize==self.empty+RIGHT:
                self.prize, self.empty = self.empty, self.prize
                self.moves += 1
            else:
                self.move_empty()
            #self.draw()
            print(" Moves: %s   "%self.moves, end='\r')
            #time.sleep(0.2)
        return self.moves
    def __contains__(self, p):
        return (0<=p[0]<self.width and 0<=p[1]<self.height)
    def __getitem__(self, pos):
        if pos==self.prize:
            return PRIZE
        if pos==self.dest:
            return DESTINATION
        if pos==self.empty:
            return EMPTY
        if pos not in self or pos in self.obstacles:
            return OBSTACLE
        return NORMAL
    def draw(self):
        for y in range(self.height):
            print(' '.join(self[x,y] for x in range(self.width)))
    def step_empty(self, direction):
        p = self.empty+direction
        if not self.can_empty_go_in(p) and direction.y < 0:
            x = self.find_row_gap(p)
            p = self.empty + (LEFT if x < p.x else RIGHT)
        if not self.can_empty_go_in(p):
            raise ValueError("This grid is more complicated than "
                                 "the one I was written to solve.")
        self.empty = p
        self.moves += 1
    def can_empty_go_in(self, pos):
        p = self[pos]
        return p in (NORMAL, DESTINATION)
    def move_empty(self):
        if self.empty.y==self.prize.y:
            return self.step_empty(DOWN)
        if self.empty.y==self.prize.y+1:
            dx = self.prize.x - 1 - self.empty.x
            step = UP if dx==0 else RIGHT if dx > 0 else LEFT
            return self.step_empty(step)
        self.step_empty(UP)
    def find_row_gap(self, p):
        if self.prize.x > p.x:
            for x in range(p.x+1, self.width):
                if self.can_empty_go_in((x, p.y)):
                    return x
        for x in range(p.x-1, -1, -1):
            if self.can_empty_go_in((x, p.y)):
                return x
        if self.prize.x <= p.x:
            for x in range(p.x+1, self.width):
                if self.can_empty_go_in((x, p.y)):
                    return x
        raise ValueError("This grid is more complicated than the one "
                             "I was written to solve.")

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
    width = max(node.position.x for node in nodes)+1
    height = max(node.position.y for node in nodes)+1
    prize = Point(width-1, 0)
    obstacles = { node.position for node in nodes if node.used > 200 }
    empty = [node for node in nodes if node.used==0]
    assert len(empty)==1
    empty = empty[0].position
    dest = Point(0,0)
    state = State(width, height, prize, dest, empty, obstacles)
    state.draw()
    m = state.find_route()
    print("Moves: %s    "%m)

if __name__ == '__main__':
    main()
