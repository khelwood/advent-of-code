#!/usr/bin/env python3

import sys
import re
from itertools import combinations, chain

class Point(tuple):
    __slots__ = ()
    def __new__(cls, x, y, z):
        return tuple.__new__(cls, (x,y,z))
    x = property(lambda self: self[0], doc='Alias for field 0')
    y = property(lambda self: self[1], doc='Alias for field 1')
    def __add__(self, other):
        return type(self)(self[0]+other[0], self[1]+other[1], self[2]+other[2])
    def __radd__(self, other):
        return type(self)(other[0]+self[0], other[1]+self[1], other[2]+self[2])
    def __sub__(self, other):
        return type(self)(self[0]-other[0], self[1]-other[1], self[2]-other[2])
    def __rsub__(self, other):
        return type(self)(other[0]-self[0], other[1]-self[1], other[2]-self[2])
    def __str__(self):
        return '(%r,%r,%r)'%self
    def __repr__(self):
        return type(self).__name__+str(self)
    def __neg__(self):
        return type(self)(-self[0], -self[1], -self[2])
    def __pos__(self):
        return self
    def __mul__(self, other):
        return type(self)(self[0]*other, self[1]*other, self[2]*other)
    def __rmul__(self, other):
        return type(self)(other*self[0], other*self[1], other*self[2])
    def __floordiv__(self, other):
        return type(self)(self[0]//other, self[1]//other, self[2]//other)
    def __truediv__(self, other):
        return type(self)(self[0]/other, self[1]/other, self[2]/other)
    def __mod__(self, other):
        return type(self)(self[0]%other, self[1]%other, self[2]%other)
    def dot(self, other):
        return (self[0]*other[0] + self[1]*other[1] + self[2]*other[2])
    @classmethod
    def of(cls, p):
        return p if isinstance(p,cls) else cls(p[0], p[1], p[2])
    @classmethod
    def max(cls, *p):
        if len(p)==1:
            p = p[0]
        return cls(max(i[0] for i in p), max(i[1] for i in p),
                       max(i[2] for i in p))
    @classmethod
    def min(cls, *p):
        if len(p)==1:
            p = p[0]
        return cls(min(i[0] for i in p), min(i[1] for i in p),
                       min(i[2] for i in p))
    @classmethod
    def abs(cls, p):
        return cls(abs(p[0]), abs(p[1]), abs(p[2]))

class Body:
    def __init__(self, pos):
        self.pos = Point.of(pos)
        self.vel = Point(0,0,0)
    def advance(self):
        self.pos += self.vel
    def potential_energy(self):
        return sum(Point.abs(self.pos))
    def kinetic_energy(self):
        return sum(Point.abs(self.vel))
    def energy(self):
        return self.potential_energy() * self.kinetic_energy()
    def __repr__(self):
        return 'pos=%r, vel=%r'%(self.pos, self.vel)

def sign(n):
    return -1 if n<0 else 0 if n==0 else 1

def apply_gravity(bodies):
    for alpha, beta in combinations(bodies, 2):
        diff = alpha.pos - beta.pos
        acc = tuple(map(sign, diff))
        alpha.vel -= acc
        beta.vel += acc

def parse_bodies(lines):
    pattern = re.compile('<x=#, y=#, z=#>'.replace(' ', r'\s*')
                             .replace('#', '(-?\d+)'))
    for line in lines:
        line = line.strip()
        if line:
            m = re.match(pattern, line)
            if not m:
                raise ValueError("Unparsable line: %r"%line)
            pos = Point.of(tuple(map(int, m.groups())))
            yield Body(pos)

def state(bodies):
    return tuple(chain.from_iterable((body.pos, body.vel) for body in bodies))

def time_step(bodies):
    apply_gravity(bodies)
    for body in bodies:
        body.advance()

def main():
    initial_data = list(sys.stdin)
    bodies = list(parse_bodies(initial_data))
    steps = 1000
    for _ in range(steps):
        time_step(bodies)
    print("Energy:", sum(body.energy() for body in bodies))
    bodies = list(parse_bodies(initial_data))
    states = {}
    for n in range(100_000):
        new_state = state(bodies)
        if new_state in states:
            print("State %s recurred at %s"%(states[new_state], n))
        states[new_state] = n
        time_step(bodies)
    print("(no repeat - need something clever)")

if __name__ == '__main__':
    main()
