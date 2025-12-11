#!/usr/bin/env python3

import sys

from collections import Counter, defaultdict

class PathCount:
    def __init__(self, basic=0, fft=0, dac=0, both=0):
        self.basic = basic
        self.fft = fft
        self.dac = dac
        self.both = both
    def __iadd__(self, other):
        self.basic += other.basic
        self.fft += other.fft
        self.dac += other.dac
        self.both += other.both
        return self
    def add_fft(self, other):
        self.fft += other.basic + other.fft
        self.both += other.dac + other.both
    def add_dac(self, other):
        self.dac += other.basic + other.dac
        self.both += other.fft + other.both

def read_input():
    links = {}
    for line in filter(bool, map(str.strip, sys.stdin)):
        k,_,vs = line.partition(':')
        links[k] = vs.strip().split()
    return links

def count_paths_simple(links):
    paths = Counter()
    paths['you'] = 1
    outs = 0
    while paths:
        newpaths = Counter()
        for pos,n in paths.items():
            for d in links[pos]:
                if d=='out':
                    outs += n
                else:
                    newpaths[d] += n
        paths = newpaths
    return outs

def count_paths_complex(links):
    paths = {'svr':PathCount(1)}
    outs = 0
    while paths:
        newpaths = defaultdict(PathCount)
        for pos,ct in paths.items():
            for d in links[pos]:
                if d=='out':
                    outs += ct.both
                elif d=='fft':
                    newpaths[d].add_fft(ct)
                elif d=='dac':
                    newpaths[d].add_dac(ct)
                else:
                    newpaths[d] += ct
        paths = newpaths
    return outs

def main():
    links = read_input()
    print(count_paths_simple(links))
    print(count_paths_complex(links))

if __name__ == '__main__':
    main()
