#!/usr/bin/env python3

"""
FUNC 14 REQUIRES z=w+12, so 13 <= z <= 21
"""

import sys

DIGITS = range(9,0,-1)
ZRANGE = range(26**2)

class AluFunc:
    def __init__(self, args):
        self.args = args
        self.cache = {}
    def __repr__(self):
        return f'AluFunc{self.args}'
    def __call__(self, *wz):
        cache = self.cache
        z= cache.get(wz)
        if z is None:
            var1, var2, var3 = self.args
            w,z = wz
            if z%26 + var2 == w:
                z //= var1
            else:
                z = 26 * (z//var1) + w + var3

            cache[wz] = z
        return z
    def possible_wz(self, out_z, wran=DIGITS, zran=ZRANGE):
        for w in wran:
            for z in zran:
                if self(w,z)==out_z:
                    yield (w,z)

def split_to_blocks(lines):
    a = 0
    for i,line in enumerate(lines):
        if line.startswith('inp '):
            if i > a:
                yield lines[a:i]
            a = i
    yield lines[a:]

def read_block_vars(block):
    assert block[4].startswith('div z ')
    assert block[5].startswith('add x ')
    assert block[15].startswith('add y ')
    return tuple(int(block[i][6:]) for i in (4,5,15))


def create_alufuncs():
    with open('data','r') as fin:
        lines = fin.read().strip().splitlines()
    argses = tuple(map(read_block_vars, split_to_blocks(lines)))
    return tuple(map(AluFunc, argses))

def main():
    funcs = create_alufuncs()
    for f in funcs:
        print(f)
    f = funcs[-2]
    for z1 in range(13,22):
        for w,z in f.possible_wz(z1):
            print(f'{w=},{z=}')

if __name__ == '__main__':
    main()
