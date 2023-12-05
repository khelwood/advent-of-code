#!/usr/bin/env python3

import sys
import functools

DIGITS = range(9,0,-1)

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

@functools.cache
def find_z(w, z, var1, var2, var3):
    x = z % 26
    z //= var1
    x += var2
    if x!=w:
        z *= 26
    y = w + var3
    y *= x
    z += y
    return z

def find_input(need_z, *args):
    for w in DIGITS:
        for z in range(676):
            if find_z(w, z, *args)==need_z:
                yield (w,z)

def solve_z(func_vars):
    ws = []
    z = 0
    for fvars in reversed(func_vars):
        for w,z in find_input(z, fvars):
            FTHIS
        wz = find_input(0, *fvars)
        if wz is None:
            return ws
        w,z=wz
        ws.insert(0, w)
    return ws


def solve(func_vars, z, index, checked=set()):
    key=(z,index)
    if key in checked:
        return None
    checked.add(key)
    if index==len(func_vars)-1:
        for w in DIGITS:
            z1 = find_z(w, z, *func_vars[index])
            if z1==1:
                return (w,)
    else:
        for w in DIGITS:
            z1 = find_z(w, z, *func_vars[index])
            seq = solve(func_vars, z1, index+1)
            if seq:
                return (w,) + seq
    return None



def main():
    with open('data') as fin:
        lines = fin.read().strip().splitlines()
    func_vars = tuple(map(read_block_vars, split_to_blocks(lines)))
    for z in func_vars:
        print(z)
    result = solve_z(func_vars)
    print(result)

if __name__ == '__main__':
    main()
