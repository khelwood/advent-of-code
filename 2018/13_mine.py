#!/usr/bin/env python3

import sys

DIRECTIONS = {
    '<' : (-1,0),
    '>' : (+1,0),
    'v' : (0,+1),
    '^' : (0,-1),
}

class Mine:
    def __init__(self, lines):
        self.carts = []
        self.lines = tuple(self.extract_carts(line, y)
                           for y,line in enumerate(lines))
        self.width = max(map(len, lines))
        self.height = len(lines)
    def extract_carts(self, line, y, directions=DIRECTIONS):
        for x in range(len(line)):
            direc = directions.get(line[x])
            if direc:
                if isinstance(line, str):
                    line = list(line)
                line[x] = '-' if direc[0] else '|'
                self.carts.append(Cart(x,y, direc))
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
    def __str__(self):
        return '\n'.join(self.lines)
    def tick_to_crash(self):
        carts = sorted(self.carts)
        positions = { cart.position: cart for cart in carts }
        for cart in carts:
            oldpos = cart.position
            cart.advance(self)
            newpos = cart.position
            if newpos in positions:
                return newpos # CRASH
            positions[newpos] = positions[oldpos]
            del positions[oldpos]
    def display(self):
        ycarts = {}
        for cart in self.carts:
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
    def __lt__(self, other):
        return (self.y < other.y or self.y==other.y and self.x < other.x)
    def __repr__(self):
        return f'Cart({self.x}, {self.y}, {self.direction})'
    @property
    def position(self):
        return (self.x, self.y)
    def advance(self, mine):
        v = mine[self.x, self.y]
        vx,vy = self.direction
        if v=='/':
            (vx,vy) = self.direction = (-vy, -vx)
        elif v=='\\':
            (vx,vy) = self.direction = (+vy, +vx)
        elif v=='+':
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
    while True:
        #mine.display()
        crash = mine.tick_to_crash()
        if crash:
            break
    print("First crash: %r,%r"%crash)

if __name__ == '__main__':
    main()
