#!/usr/bin/env python3

import sys

DIRECTIONS = { '<' : (-1,0), '>' : (+1,0), 'v' : (0,+1), '^' : (0,-1), }

class Mine:
    def __init__(self, lines):
        self.pos_carts = {}
        self.lines = tuple(self.extract_carts(line, y)
                           for y,line in enumerate(lines))
        self.width = max(map(len, lines))
        self.height = len(lines)
        self.first_crash = None
    def extract_carts(self, line, y, directions=DIRECTIONS):
        for x in range(len(line)):
            direc = directions.get(line[x])
            if direc:
                if isinstance(line, str):
                    line = list(line)
                line[x] = '-' if direc[0] else '|'
                self.pos_carts[x,y] = Cart(x, y, direc)
        if isinstance(line, list):
            line = ''.join(line)
        return line
    def __getitem__(self, p):
        x,y = p
        if 0 <= y < len(self.lines):
            line = self.lines[y]
            if 0 <= x < len(line):
                return line[x]
        return ' '
    @property
    def num_carts(self):
        return len(self.pos_carts)
    def tick(self):
        pos_carts = self.pos_carts
        for cart in sorted(pos_carts.values()):
            if cart.crashed:
                continue
            del pos_carts[cart.position]
            cart.advance(self)
            newpos = cart.position
            if newpos in pos_carts:
                if self.first_crash is None:
                    self.first_crash = newpos
                other = pos_carts.pop(newpos)
                other.crashed = True
                cart.crashed = True
            else:
                pos_carts[newpos] = cart
    def display(self):
        ycarts = {}
        for cart in self.pos_carts.values():
            if cart.y not in ycarts:
                ycarts[cart.y] = []
            ycarts[cart.y].append(cart)
        dir_rev = {v:k for (k,v) in DIRECTIONS.items()}
        for y,line in enumerate(self.lines):
            if y not in ycarts:
                print(line)
                continue
            line = list(line)
            for cart in ycarts[y]:
                line[cart.x] = dir_rev[cart.direction]
            print(''.join(line))

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turns = 0
        self.crashed = False
    def __lt__(self, other):
        return (self.y < other.y or self.y==other.y and self.x < other.x)
    @property
    def position(self):
        return (self.x, self.y)
    def advance(self, mine):
        track = mine[self.x, self.y]
        vx,vy = self.direction
        if track=='/':
            (vx,vy) = self.direction = (-vy, -vx)
        elif track=='\\':
            (vx,vy) = self.direction = (+vy, +vx)
        elif track=='+':
            if self.turns==0:
                self.turns = 1
                (vx,vy) = self.direction = (vy,-vx)
            elif self.turns==1:
                self.turns = 2
            else:
                self.turns = 0
                (vx,vy) = self.direction = (-vy,vx)
        self.x += vx
        self.y += vy

def main():
    mine = Mine(sys.stdin.read().splitlines())
    while mine.first_crash is None:
        #mine.display()
        mine.tick()
    print("First crash: %r,%r"%mine.first_crash)
    while mine.num_carts > 1:
        mine.tick()
    print("Last cart position: %r,%r"%next(iter(mine.pos_carts)))

if __name__ == '__main__':
    main()
