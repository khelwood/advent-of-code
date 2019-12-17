#!/usr/bin/env python3

import sys

PATTERN = (0,1,0,-1)

class Pattern:
    def __init__(self, pattern, repeats):
        self.length = len(pattern) * repeats
        self.pattern = pattern
        self.repeats = repeats
    def __len__(self):
        return self.length
    def __getitem__(self, index):
        pos = (index+1) % self.length
        return self.pattern[pos // self.repeats]
    def __call__(self, data):
        return abs(sum(a*b for a,b in zip(self, data)))%10

def main():
    signal = tuple(map(int, sys.stdin.read().strip()))
    print("Input signal:", ''.join(map(str, signal)))
    patterns = [Pattern(PATTERN, i+1) for i in range(len(signal))]
    for phase in range(100):
        print(' ', phase, ' ', end='\r')
        signal = tuple(p(signal) for p in patterns)
    print("Signal after 100 phases:", ''.join(map(str, signal)))

if __name__ == '__main__':
    main()
