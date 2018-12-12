#!/usr/bin/env python3

import sys

class PlantRow:
    def __init__(self):
        self.on = set()
        self.min = 0
        self.max = 0
    def __getitem__(self, index):
        return (index in self.on)
    def __setitem__(self, index, value):
        if value:
            if index not in self.on:
                self.min = min(self.min, index)
                self.max = max(self.max, index)
                self.on.add(index)
        else:
            if index in self.on:
                self.on.remove(index)
                if index==self.min:
                    self.min = min(self.on)
                if index==self.max:
                    self.max = max(self.on)
    def __str__(self):
        return ''.join(['#' if self[i] else '.'
                        for i in range(self.min, self.max+1)])
    def advance(self, moves):
        new = PlantRow()
        jran = range(-2, 3)
        for i in range(self.min-2, self.max+3):
            code = tuple(self[i+j] for j in jran)
            if moves.get(code):
                new[i] = True
        return new
    def sum(self):
        return sum(self.on)

def read_data():
    lines = sys.stdin.read().splitlines()
    state = PlantRow()
    moves = {}
    for line in lines:
        line = line.strip()
        if line.startswith('initial state:'):
            line = line.partition(':')[2].strip()
            for i,v in enumerate(line):
                state[i] = (v=='#')
        elif line:
            code,_,result = map(str.strip, line.partition('=>'))
            code = tuple(v=='#' for v in code)
            result = (result=='#')
            moves[code] = result
    return state, moves

def main():
    state, moves = read_data()
    for _ in range(20):
        state = state.advance(moves)
    print(state.sum())
    for _ in range(50_000_000_000 - 20):
        state = state.advance(moves)
    print(state.sum())

if __name__ == '__main__':
    main()
