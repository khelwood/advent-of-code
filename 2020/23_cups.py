#!/usr/bin/env python3

import sys
import itertools

class Cups:
    def __init__(self, values, size=None):
        path = [None]*((size or len(values))+1)
        last = 0
        for v in values:
            path[last] = v
            last = v
        path[last] = path[0]
        self.path = path

    def __iter__(self):
        path = self.path
        cur = path[0]
        yield cur
        v = path[cur]
        while v != cur:
            yield v
            v = path[v]

    def __repr__(self):
        return ' '.join(map(str, self))

    def __str__(self):
        lines = [
            ' '.join(map(str, range(len(self.path)))),
            ' '.join('↓' for _ in self.path),
            ' '.join(map(str, self.path)),
            'Giving:',
            ' '.join(map(str, self)),
        ]
        return '\n'.join(lines)

    @property
    def code(self):
        path = self.path
        vals = []
        v = path[1]
        while v != 1:
            vals.append(v)
            v = path[v]
        return ''.join(map(str, vals))

    def move(self):
        path = self.path
        cur = path[0]
        first = path[cur]
        second = path[first]
        third = path[second]
        n = len(path)-1
        skip = {first, second, third}
        dest = (cur-1)
        if dest < 1:
            dest = n
        while dest in skip:
            dest -= 1
            if dest < 1:
                dest = n
        path[cur] = path[third]
        path[third] = path[dest]
        path[dest] = first
        path[0] = path[cur]


def main():
    arg = sys.argv[1] if len(sys.argv)>1 else input()
    initial = tuple(map(int, arg))
    cups = Cups(initial)
    for _ in range(100):
        cups.move()
    print(cups.code)
    M = 1_000_000
    cups = Cups(itertools.chain(initial, range(10, M+1)), size=M)
    for i in range(100):
        print(f' {i}%', end='\r',flush=True)
        for _ in range(100_000):
            cups.move()
    print('100 %')
    a = cups.path[1]
    b = cups.path[a]
    print(a*b)


if __name__ == '__main__':
    main()
