#!/usr/bin/env python3

import sys
from knothash import Loop

def main():
    if len(sys.argv)<=1:
        exit("Usage: %s <lengths>"%sys.argv[0])
    data = ','.join(sys.argv[1:]).replace(' ','').replace(',,',',')
    lengths = [int(n) for n in data.split(',')]
    loop = Loop()
    loop.apply_twists(lengths)
    print("Part 1.")
    #print("Loop:", loop)
    print("Product of first two numbers:", loop[0]*loop[1])
    print()
    print("Part 2.")
    lengths = [ord(ch) for ch in data] + [17, 31, 73, 47, 23]
    loop = Loop()
    loop.apply_twists(lengths, 64)
    #print("Loop:", loop)
    kh = loop.knothash()
    print("Knot hash:", kh)

if __name__ == '__main__':
    main()
