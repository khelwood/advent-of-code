#!/usr/bin/env python3

import sys
import itertools

ROCK = '#'

ROCKS = '''
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''

WID = 7

class Rock:
    def __init__(self, wid, hei, solid, position=(0,0)):
        self.wid = wid
        self.hei = hei
        self.solid = solid
        self.position = position
    @property
    def position(self):
        return (self.x, self.y)
    @position.setter
    def position(self, value):
        self.x, self.y = value
    def __contains__(self, p):
        return ((p[0]-self.x, p[1]-self.y) in self.solid)
    def jet(self, dx):
        self.x += dx
    def retract(self, dx):
        self.x -= dx
    def fall(self):
        self.y += 1
    def rise(self):
        self.y -= 1
    def __iter__(self):
        x = self.x
        y = self.y
        return ((px+x, py+y) for (px,py) in self.solid)
    @property
    def left(self):
        return self.x
    @property
    def right(self):
        return self.x + self.wid - 1
    @property
    def top(self):
        return self.y
    @property
    def bottom(self):
        return self.y + self.hei - 1
    def overlaps(self, solid):
        return any(r in solid for r in self)

def parse_rocks():
    rocks = []
    for block in map(str.strip, ROCKS.split('\n\n')):
        lines = block.splitlines()
        wid = len(lines[0])
        hei = len(lines)
        solid = set()
        for y,line in enumerate(lines):
            for x,ch in enumerate(line):
                if ch==ROCK:
                    solid.add((x,y))
        rocks.append(Rock(wid, hei, solid))
    return rocks

def rock_fall(rock, highest, ground, flow_cycle):
    rock.position = (2, highest - 3 - rock.hei)
    #print("ROCK INITIAL POSITION:", rock.offset)
    for flow in flow_cycle:
        rock.jet(flow)
        if rock.left < 0 or rock.right >= WID or rock.overlaps(ground):
            rock.retract(flow)
        #print("JET -> ROCK OFFSET:", rock.offset)
        rock.fall()
        if rock.overlaps(ground):
            rock.rise()
            break
        #print("FALL-> ROCK OFFSET:", rock.offset)
    #print("FINAL ROCK OFFSET:", rock.offset)
    ground.update(rock)
    return min(highest, rock.top)

def draw_solid(ground, highest):
    print()
    for y in range(highest, 0):
        print('% 3d\t|%s|'%(y,''.join(ROCK if (x,y) in ground else '.' for x in range(WID))))
    print('% 3d\t|%s|'%(0, '-'*WID))

def main():
    rocks = parse_rocks()
    flows = tuple(1 if ch=='>' else -1 for ch in sys.stdin.read().strip())
    flow_cycle = itertools.cycle(flows)
    ground = {(x,0) for x in range(WID)}
    highest = 0
    rock_cycle = itertools.cycle(rocks)
    for _ in range(2022):
        highest = rock_fall(next(rock_cycle), highest, ground, flow_cycle)
    draw_solid(ground, -10)
    print("Height:", -highest)

if __name__ == '__main__':
    main()
