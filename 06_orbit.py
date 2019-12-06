#!/usr/bin/env python3

import sys

class Body:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self._depth = None
    @property
    def depth(self):
        if self._depth is None:
            self._depth = self.parent.depth + 1
        return self._depth

def parse_orbits(string):
    com = Body('COM')
    com._depth = 0
    bodies = {'COM': com}
    for line in string.splitlines():
        if ')' in line:
            a,b = line.split(')')
            body_a = bodies.get(a)
            if body_a is None:
                body_a = Body(a)
                bodies[a] = body_a
            body_b = bodies.get(b)
            if body_b is None:
                body_b = Body(b)
                bodies[b] = body_b
            body_b.parent = body_a
    return bodies

def count_transfers(src, dst):
    n = 0
    while src.depth > dst.depth:
        n += 1
        src = src.parent
    while dst.depth > src.depth:
        n += 1
        dst = dst.parent
    while src != dst:
        n += 2
        src = src.parent
        dst = dst.parent
    return n - 2

def main():
    bodies = parse_orbits(sys.stdin.read())
    num_orbits = sum(body.depth for body in bodies.values())
    print("Number of direct and indirect orbits:", num_orbits)
    num_transfers = count_transfers(bodies['YOU'], bodies['SAN'])
    print("Number of transfers:", num_transfers)

if __name__ == '__main__':
    main()
