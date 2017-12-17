#!/usr/bin/env python3

import sys

class Spinlock:
    def __init__(self, step_size):
        self.step_size = step_size
        self.buffer = [0]
        self.position = 0
        self.next_value = 1
    def advance(self):
        p = (self.position+self.step_size) % len(self.buffer)
        self.buffer.insert(p+1, self.next_value)
        self.position = p+1
        self.next_value += 1
    def __str__(self):
        return '['+' '.join('(%s)'%v if i==self.position else str(v)
                        for i,v in enumerate(self.buffer)) + ']'

def fast_spinlock(step_size, count):
    pos = 0
    size = 1
    after_zero = 0
    for value in range(1, count+1):
        pos = (pos+step_size)%size
        if pos==0:
            after_zero = value
        pos += 1
        size += 1
    return after_zero

def main(step_size):
    sl = Spinlock(step_size)
    for _ in range(2017):
        sl.advance()
    print("Value after 2017:", sl.buffer[(sl.position+1)%len(sl.buffer)])
    print(' ...', end='\r')
    v = fast_spinlock(step_size, 50_000_000)
    print("Value after zero:", v)

if __name__ == '__main__':
    if len(sys.argv)!=2:
        exit("Usage: %s <number>"%sys.argv[0])
    main(int(sys.argv[1]))
