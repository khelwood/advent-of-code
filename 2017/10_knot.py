#!/usr/bin/env python3

import sys
import functools
import operator

PART=2

MY_DATA = '189,1,111,246,254,2,0,120,215,93,255,50,84,15,94,62'
LOOP_LEN = 256

def twist(loop, length, cur, skip):
    L = len(loop)
    for i in range(length//2):
        p = (cur + i) % L
        q = (cur + length - i - 1) % L
        loop[p], loop[q] = loop[q], loop[p]
    cur = (cur + length + skip)%L
    skip = (skip + 1)%L
    return cur, skip

def show(loop, cur):
    return '('+' '.join(['[%r]'%x if i==cur else repr(x)
                            for i,x in enumerate(loop)]) + ')'

def convert(loop):
    dense = [functools.reduce(operator.xor, loop[i:i+16])
                 for i in range(0, len(loop), 16)]
    return ''.join([format(n, '02x') for n in dense])
        
def main(data, loop_len):
    print("Data:", data)
    if PART<2:
        lengths = [int(n) for n in data.replace(',',' ').split()]
        repeats = 1
    else:
        lengths = [ord(ch) for ch in data.strip()] + [17, 31, 73, 47, 23]
        repeats = 64
    loop = list(range(loop_len))
    cur = 0
    skip = 0
    for _ in range(repeats):
        for length in lengths:
            #print(show(loop, cur))
            cur, skip = twist(loop, length, cur, skip)
    if PART<2:
        print("Result:", show(loop, cur))
        print("Product of first two numbers:", loop[0]*loop[1])
    else:
        print("Loop data:", show(loop, cur))
        result = convert(loop)
        print("Result:", result)

if __name__ == '__main__':
    data = sys.argv[1] if len(sys.argv) > 1 else MY_DATA
    loop_len = int(sys.argv[2]) if len(sys.argv) > 2 else LOOP_LEN
    main(data, loop_len)
