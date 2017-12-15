#!/usr/bin/env python3

import sys
import re

CUBOID_PTN = re.compile('^#x#x#$'.replace('#', '([0-9]+)'))

def make_cuboid(line):
    m = re.match(CUBOID_PTN, line)
    if not m:
        raise ValueError(repr(line))
    return sorted(int(m.group(i)) for i in range(1,4))

def paper(cuboid):
    a,b,c = cuboid
    return 2*(a*(b+c)+b*c)+a*b

def ribbon(cuboid):
    a,b,c = cuboid
    return 2*(a+b) + a*b*c

def main():
    lines = sys.stdin.read().strip().split('\n')
    cuboids = [make_cuboid(line) for line in lines]
    total_paper = sum(map(paper, cuboids))
    print("Total paper:", total_paper)
    total_ribbon = sum(map(ribbon, cuboids))
    print("Total ribbon:", total_ribbon)

if __name__ == '__main__':
    main()
