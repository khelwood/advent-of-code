import sys

DIRECTIONS = {'>':(1,0), 'v':(0,1)}

class Sea:
    def __init__(self, size, herds):
        self.size = size
        self.herds = herds
    
    def run_herd(self, dir):
        herd = self.herds[dir]
        new_herd = set()
        dx,dy = dir
        w,h = self.size
        any_moved = False
        for p in herd:
            x,y = p
            n = ((x+dx)%w, (y+dy)%h)
            if any(n in h for h in self.herds.values()):
                new_herd.add(p)
            else:
                new_herd.add(n)
                any_moved = True
        if not any_moved:
            return False
        self.herds[dir] = new_herd
        return True
    
    def run(self):
        turns = 1
        dirs = tuple(DIRECTIONS[ch] for ch in '>v')
        while sum(map(self.run_herd, dirs)) > 0:
            turns += 1
        return turns


def read_sea(lines):
    herds = {v:set() for v in DIRECTIONS.values()}
    for y,line in enumerate(lines):
        for x,ch in enumerate(line):
            if ch != '.':
                herds[DIRECTIONS[ch]].add((x,y))
    return Sea((len(lines[0]), len(lines)), herds)

def main():
    sea = read_sea(sys.stdin.read().strip().splitlines())
    print(sea.run())

if __name__ == '__main__':
    main()
