#!/usr/bin/env python3

import sys
import itertools

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def addp(a, b):
    return (a[0]+b[0], a[1]+b[1])

STEP_DICT = {
    'D': lambda dist: (0, dist),
    'L': lambda dist: (-dist, 0),
    'R': lambda dist: (dist, 0),
    'U': lambda dist: (0, -dist),
}

class Pos:
    def __init__(self, x, y, steps):
        self._x = x
        self._y = y
        self._steps = steps
    x = property(lambda self: self._x)
    y = property(lambda self: self._y)
    steps = property(lambda self: self._steps)
    manhattan = property(lambda self: abs(self.x) + abs(self.y))
    def __add__(self, other):
        dx,dy = other
        x = self.x + dx
        y = self.y + dy
        steps = self.steps + abs(dx) + abs(dy)
        return Pos(x,y,steps)
    def __getitem__(self, index):
        if index==0:
            return self.x
        if index==1:
            return self.y
        raise ValueError("Invalid Pos index %r"%index)
    def __repr__(self):
        return f"Pos({self.x}, {self.y}, {self.steps})"
    def steps_to(self, point):
        px, py = point
        return self.steps + abs(px-self.x) + abs(py-self.y)

class Line:
    def __init__(self, start, end):
        self._start = start
        self._end = end
    start = property(lambda self: self._start)
    end = property(lambda self: self._end)
    vertical = property(lambda self: self.start.x==self.end.x)
    horizontal = property(lambda self: self.start.y==self.end.y)
    def __len__(self):
        return abs(self.start.x-self.end.x) + abs(self.start.y-self.end.y)
    def __getitem__(self, index):
        if index==0:
            return self.start
        if index==1:
            return self.end
        raise ValueError("Invalid Line index %r"%index)
    def __repr__(self):
        return f"Line({self.start}, {self.end})"
    minx = property(lambda self: min(self.start.x, self.end.x))
    maxx = property(lambda self: max(self.start.x, self.end.x))
    miny = property(lambda self: min(self.start.y, self.end.y))
    maxy = property(lambda self: max(self.start.y, self.end.y))
        

def parse_step(string):
    ch = string[0]
    dist = int(string[1:])
    return STEP_DICT[ch](dist)

def parse_path(line):
    return [parse_step(step) for step in line.replace(',',' ').split()]

def path_lines(path):
    pos = Pos(0,0,0)
    for step in path:
        next_pos = pos + step
        yield Line(pos, next_pos)
        pos = next_pos

def vertical(line):
    return line[0][0]==line[1][0]

def intersection(la, lb):
    if la.vertical:
        if lb.vertical:
            return None
        la, lb = lb, la
    elif lb.horizontal:
        return None
    # Now line1 is horizontal and line2 is vertical
    x = lb.start.x
    y = la.start.y
    if la.minx > x or la.maxx < x:
        return None
    if lb.miny > y or lb.maxy < y:
        return None
    # x,y is the point of intersection, but how many steps is it?
    steps = la.start.steps_to((x,y)) + lb.start.steps_to((x,y))
    return Pos(x, y, steps)

def find_intersections(path1, path2):
    lines1 = list(path_lines(path1))
    lines2 = list(path_lines(path2))
    for line1, line2 in itertools.product(lines1, lines2):
        sect = intersection(line1, line2)
        if sect:
            yield sect
            
def find_closest_intersection_distance(path1, path2):
    closest = None
    for p in find_intersections(path1, path2):
        dist = p.manhattan
        if dist and (closest is None or dist < closest):
            closest = dist
    return closest

def find_least_steps_intersection(path1, path2):
    least = None
    for p in find_intersections(path1, path2):
        if not(p.x==0==p.y) and (least is None or p.steps < least):
            least = p.steps
    return least

def main():
    path1, path2 = (parse_path(line) for line in sys.stdin.read().splitlines())
    d = find_closest_intersection_distance(path1, path2)
    print("Closest:", d)
    s = find_least_steps_intersection(path1, path2)
    print("Least steps:", s)

if __name__ == '__main__':
    main()
