#!/usr/bin/env python3

import sys
import itertools

def new_bug(is_bug, neighbours):
    return (neighbours==1 or not is_bug and neighbours==2)

class BugGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bugs = set()
    def add_bug(self, p):
        self.bugs.add(p)
    def __contains__(self, p):
        return (p in self.bugs)
    def count_near(self, p):
        x,y = p
        return sum(q in self for q in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)))
    def positions(self):
        return itertools.product(range(self.width), range(self.height))
    def next_gen(self, func):
        new_bugs = set()
        for p in self.positions():
            if func(p in self, self.count_near(p)):
                new_bugs.add(p)
        return new_bugs
    def advance(self, func):
        self.bugs = self.next_gen(func)
    def rating(self):
        wid = self.width
        total = 0
        for (x,y) in self.bugs:
            i = x + wid * y
            total += (1<<i)
        return total

def neighbours(pos, ran=range(5)):
    x,y,z = pos
    if y==0:
        yield 2,1,z-1
        yield x,1,z
    elif y==4:
        yield x,3,z
        yield 2,3,z-1
    elif x!=2:
        yield x,y-1,z
        yield x,y+1,z
    elif y==1:
        # 2,1
        yield 2,0,z
        yield from ((xx,0,z+1) for xx in ran)
    elif y==3:
        # 2,3
        yield from ((xx,4,z+1) for xx in ran)
        yield 2,4,z

    if x==0:
        yield 1,2,z-1
        yield 1,y,z
    elif x==4:
        yield 3,y,z
        yield 3,2,z-1
    elif y!=2:
        yield x-1,y,z
        yield x+1,y,z
    elif x==1:
        # 1,2: square 12
        yield 0,2,z
        yield from ((0, yy, z+1) for yy in ran)
    elif x==3:
        # 3,2: square 14
        yield from ((4, yy, z+1) for yy in ran)
        yield 4,2,z



class BugTower:
    def __init__(self, initial_bugs):
        self.bugs = {(x,y,0) for (x,y) in initial_bugs}
    def next_gen(self):
        bugs = self.bugs
        neighbours_of_bugs = {nbr for p in bugs for nbr in neighbours(p)} - bugs
        new_bugs = set()
        infection = {1,2}
        for p in bugs:
            if sum((nbr in bugs) for nbr in neighbours(p))==1:
                new_bugs.add(p)
        for n in neighbours_of_bugs:
            if sum((nbr in bugs) for nbr in neighbours(n)) in infection:
                new_bugs.add(n)
        return new_bugs
    def advance(self):
        self.bugs = self.next_gen()


def parse_grid(string):
    lines = string.splitlines()
    width = len(lines[0])
    height = len(lines)
    bugs = BugGrid(width, height)
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch=='#':
                bugs.add_bug((x,y))
    return bugs

def main():
    bugs = parse_grid(sys.stdin.read())
    initial_bugs = set(bugs.bugs)
    ratings = {bugs.rating()}
    while True:
        bugs.advance(new_bug)
        rating = bugs.rating()
        if rating in ratings:
            break
        ratings.add(rating)
    print("Repeated rating:", rating)

    bugs = BugTower(initial_bugs)
    for i in range(200):
        bugs.advance()
    print("Bugs in tower:", len(bugs.bugs))


if __name__ == '__main__':
    main()
