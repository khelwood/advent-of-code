#!/usr/bin/env python3

import sys
from ast import literal_eval as leval
from itertools import permutations

class Sf:
    __slots__ = ('parent', 'left', 'right')

    def __init__(self, par=None):
        self.parent = par
        self.left = None
        self.right = None

    def add_right(self, value):
        c = self
        p = c.parent
        while p and c is p.right:
            c = p
            p = c.parent
        if p is None:
            return False
        if isinstance(p.right, int):
            p.right += value
            return True
        p = p.right
        while isinstance(p.left, Sf):
            p = p.left
        p.left += value
        return True

    def add_left(self, value):
        c = self
        p = c.parent
        while p and c is p.left:
            c = p
            p = c.parent
        if p is None:
            return False
        if isinstance(p.left, int):
            p.left += value
            return True
        p = p.left
        while isinstance(p.right, Sf):
            p = p.right
        p.right += value
        return True

    def replace(self, value):
        if self is self.parent.left:
            self.parent.left = value
        elif self is self.parent.right:
            self.parent.right = value

    def explode(self):
        self.add_left(self.left)
        self.add_right(self.right)
        self.replace(0)

    def split_left(self):
        self.left = self.split(self.left)

    def split_right(self):
        self.right = self.split(self.right)

    def split(self, value):
        sf = Sf(self)
        sf.left = value//2
        sf.right = (value+1)//2
        return sf

    def find_explode(self, depth=0):
        if depth==4:
            return self
        if isinstance(self.left, Sf):
            n = self.left.find_explode(depth+1)
            if n:
                return n
        if isinstance(self.right, Sf):
            n = self.right.find_explode(depth+1)
            if n:
                return n
        return None

    def find_split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                return self, 'L'
        else:
            n,d = self.left.find_split()
            if n:
                return (n,d)
        if isinstance(self.right, int):
            if self.right >= 10:
                return self, 'R'
        else:
            n,d = self.right.find_split()
            if n:
                return (n,d)
        return None,None

    def reduce(self):
        while True:
            n = self.find_explode()
            if n:
                n.explode()
                continue
            n,side = self.find_split()
            if n:
                if side=='R':
                    n.split_right()
                else:
                    n.split_left()
                continue
            break

    @classmethod
    def parse(cls, value, par=None):
        if not isinstance(value, list):
            return value
        sf = cls(par)
        sf.left = cls.parse(value[0], sf)
        sf.right = cls.parse(value[1], sf)
        return sf

    def __add__(self, other):
        assert not self.parent
        p = Sf()
        if isinstance(other, Sf):
            assert not other.parent
            other.parent = p
        self.parent = p
        p.left = self
        p.right = other
        return p

    def magnitude(self):
        n = self.left
        r = self.right
        if isinstance(n, Sf):
            n = n.magnitude()
        if isinstance(r, Sf):
            r = r.magnitude()
        return 3*n + 2*r

    def __repr__(self):
        return f'[{self.left},{self.right}]'


def main():
    original_data = tuple(map(leval, sys.stdin.read().strip().splitlines()))
    sfs = list(map(Sf.parse, original_data))
    it = iter(sfs)
    total = next(it)
    for sf in it:
        total += sf
        total.reduce()
    print("Total magnitude:", total.magnitude())
    best = 0
    for a,b in permutations(original_data, 2):
        total = Sf.parse(a) + Sf.parse(b)
        total.reduce()
        best = max(best, total.magnitude())
    print("Best magnitude:", best)

if __name__ == '__main__':
    main()
