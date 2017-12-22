#!/usr/bin/env python3

import sys

class Infection:
    def __init__(self, position):
        self._infected = {}
        self.position = position
        self.direc = (0,-1)
        self.infection_count = 0
    def __len__(self):
        return len(self._infected)
    @property
    def current(self):
        return self._infected.get(self.position, None)
    @current.setter
    def current(self, value):
        self._infected[self.position] = value
    def step(self):
        self.position = (self.position[0]+self.direc[0],
                         self.position[1]+self.direc[1])
    def turn_left(self):
        self.direc = (self.direc[1], -self.direc[0])
    def turn_right(self):
        self.direc = (-self.direc[1], self.direc[0])
    def burst(self):
        cur = self.current
        if cur:
            self.turn_left()
            self.current = None
        else:
            self.turn_right()
            self.current = '#'
            self.infection_count += 1
        self.step()
    def load(self, lines):
        for y,line in enumerate(lines):
            for x,ch in enumerate(line):
                if ch=='#':
                    self._infected[x,y] = ch

class EvolvedInfection(Infection):
    def turn_around(self):
        self.direc = (-self.direc[0], -self.direc[1])
    def burst(self):
        cur = self.current
        if not cur:
            self.current = 'W'
            self.turn_left()
        elif cur=='#':
            self.current = 'F'
            self.turn_right()
        elif cur=='F':
            self.current = None
            self.turn_around()
        else:
            self.current = '#'
            self.infection_count += 1
        self.step()
        
def main():
    lines = sys.stdin.read().strip().split('\n')
    start_pos = (len(lines[0])//2, len(lines)//2)
    infection = Infection(start_pos)
    infection.load(lines)
    for i in range(10_000):
        infection.burst()
        if i%100==0:
            print('',i,end='\r')
    print("Simple infection count:", infection.infection_count)
    infection = EvolvedInfection(start_pos)
    infection.load(lines)    
    for i in range(10_000_000):
        infection.burst()
        if i%100_000==0:
            print('',i,end='\r')
    print("Evolved infection count:", infection.infection_count)

if __name__ == '__main__':
    main()

    #(Total time: 33.52374196052551)
