import sys

DIRECTIONS = {'>':(1,0), 'v':(0,1)}

class Sea:
    def __init__(self, wid, hei, herds):
        self.wid = wid
        self.hei = hei
        self.herds = herds
        self.occupied = {c.pos for herd in herds for c in herd}
    
    def predict_move(self, critter):
        x,y = critter.pos
        dx,dy = critter.dir
        nextpos = ((x+dx)%self.wid, (y+dy)%self.hei)
        if nextpos in self.occupied:
            nextpos = None
        critter.next = nextpos
        return nextpos
    
    def execute_move(self, critter):
        n = critter.next
        if n is not None:
            self.occupied.remove(critter.pos)
            self.occupied.add(n)
            critter.pos = n
    
    def move_herd(self, herd):
        crs = [c for c in herd if self.predict_move(c)]
        if not crs:
            return False
        for c in crs:
            self.execute_move(c)
        return True
    
    def run(self):
        herds = self.herds
        turns = 1
        while sum(self.move_herd(herd) for herd in herds) > 0:
            turns += 1
        return turns


class Critter:
    def __init__(self, dir, pos):
        self.dir = dir
        self.pos = pos
        self.next = None

def read_sea(lines):
    herds = {v:[] for v in DIRECTIONS}
    for y, line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch != '.':
                pos = (x,y)
                dir = DIRECTIONS[ch]
                cr = Critter(dir, pos)
                herds[ch].append(cr)
    return Sea(len(lines[0]), len(lines), [herds[ch] for ch in '>v'])
    

def main():
    lines = sys.stdin.read().strip().splitlines()
    sea = read_sea(lines)
    print(sea.run())

if __name__ == '__main__':
    main()
