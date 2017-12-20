#!/usr/bin/env python3

import sys
import re

class NPoint(tuple):
    """Quick implementation of an immutable n-dimensional point."""
    __slots__ = ()
    def __neg__(self):
        return type(self)(-x for x in self)
    def __pos__(self):
        return self
    def __add__(self, other):
        return type(self)(self[i] + other[i] for i in range(len(self)))
    __radd__ = __add__
    def __sub__(self, other):
        return type(self)(self[i] - other[i] for i in range(len(self)))
    def __rsub__(self, other):
        return type(self)(other[i] - self[i] for i in range(len(self)))
    def __mul__(self, scale):
        return type(self)(scale*x for x in self)
    __rmul__ = __mul__

def manhattan(p):
    return sum(map(abs, p))

class Particle:
    def __init__(self, index, pos, vel, acc):
        self.index = index
        self.pos = pos
        self.vel = vel
        self.acc = acc
    def accelerate(self):
        self.vel += self.acc
    def travel(self):
        self.pos += self.vel
    def update(self):
        self.accelerate()
        self.travel()
    def position_after(self, time):
        return self.pos + self.vel*time + self.acc*(time*time)
    def __repr__(self):
        return 'Particle(%s)'%self.index

PARTICLE_PTN = re.compile(r'p=<>,\s*v=<>,\s*a=<>'.replace(
    '<>', '<'+r','.join(3*[r'\s*(-?[0-9]+)'])+'>'))

def parse_particle(i, line):
    m = PARTICLE_PTN.match(line)
    assert m, line
    p = NPoint(int(m.group(i)) for i in range(1,4))
    v = NPoint(int(m.group(i)) for i in range(4,7))
    a = NPoint(int(m.group(i)) for i in range(7,10))
    return Particle(i, p,v,a)

def main():
    lines = sys.stdin.read().strip().split('\n')
    particles = [parse_particle(i, line) for i,line in enumerate(lines)]
    late_positions = [pa.position_after(1_000_000) for pa in particles]
    late_distances = [manhattan(pos) for pos in late_positions]
    nearest = min(late_distances)
    nearest_i = [i for i,d in enumerate(late_distances) if d==nearest]
    print("Nearest particles", nearest_i)
    # Part 2: collisions
    print("Running for collisions...")
    for i in range(200):
        collisions = set()
        positions = {}
        to_remove = set()
        for p in particles:
            p.update()
            if p.pos in collisions:
                to_remove.add(p)
                continue
            if p.pos in positions:
                collisions.add(p.pos)
                to_remove.add(p)
                to_remove.add(positions[p.pos])
                continue
            positions[p.pos] = p
        if to_remove:
            particles = [pa for pa in particles if pa not in to_remove]
    print("Num particles left after collisions:", len(particles))

if __name__ == '__main__':
    main()
