#!/usr/bin/env python3

import sys

STEPS = {'U':(0,-1), 'R':(1,0), 'D':(0,1), 'L':(-1,0)}

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def subp(a,b):
    return (a[0]-b[0], a[1]-b[1])

def tail_vec(h, t):
    x,y = subp(h,t)
    if abs(x) <= 1 and abs(y) <= 1:
        return (0,0)
    return sign(x), sign(y)

def sign(v):
    return 0 if v==0 else 1 if v>0 else -1

def read_steps():
    for line in sys.stdin:
        line = line.strip()
        if line:
            d,n = line.split()
            step = STEPS[d]
            for _ in range(int(n)):
                yield step

def trace_tail(steps):
    head = tail = (0,0)
    tail_set = {tail}
    for step in steps:
        head = addp(head, step)
        tail = addp(tail, tail_vec(head, tail))
        tail_set.add(tail)
    return tail_set

def trace_tails(steps, length):
    rope = [(0,0)]*length
    tail_set = {rope[-1]}
    for step in steps:
        for i,p in enumerate(rope):
            if i == 0:
                last = addp(p, step)
            else:
                last = addp(p, tail_vec(last, p))
            rope[i] = last
        tail_set.add(last)
    return tail_set

def main():
    steps = list(read_steps())
    tail_set = trace_tail(steps)
    print("Positions:", len(tail_set))
    tail_set = trace_tails(steps, 10)
    print("Positions:", len(tail_set))

if __name__ == '__main__':
    main()
