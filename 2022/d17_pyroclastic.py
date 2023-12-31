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

class Ground:
    def __init__(self):
        self._ground = {(x,0) for x in range(WID)}
        self._xheight = [0]*WID
        self._height = 0
        self._shape = [0]*WID

    def add(self, pos):
        x,y = pos
        self._ground.add(pos)
        self._xheight[x] = min(self._xheight[x], y)
        self._height = None
        self._shape = None

    def update(self, ps):
        for p in ps:
            self._ground.add(p)
            x,y = p
            self._xheight[x] = min(self._xheight[x], y)
        self._height = None
        self._shape = None

    @property
    def height(self):
        h = self._height
        if h is None:
            h = self._height = min(self._xheight)
        return h

    @property
    def shape(self):
        s = self._shape
        if s is None:
            xhs = self._xheight
            h = self.height
            s = self._shape = [h-xh for xh in xhs]
        return s

    def __contains__(self, pos):
        return (pos in self._ground)


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

    def fall(self, dy):
        self.y += dy

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

    def overlaps(self, solid):
        return any(r in solid for r in self)


class CountCycle:
    def __init__(self, items):
        self.items = items
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        n = self.count
        self.count += 1
        return self.items[n%len(self.items)]

    def __len__(self):
        return len(self.items)

    @property
    def key(self):
        return self.count%len(self.items)

    def reset(self):
        self.count = 0


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

def rock_fall(rock, ground, flow_cycle):
    rock.position = (2, ground.height - 3 - rock.hei)
    for flow in flow_cycle:
        rock.jet(flow)
        if rock.left < 0 or rock.right >= WID or rock.overlaps(ground):
            rock.jet(-flow)
        rock.fall(1)
        if rock.overlaps(ground):
            rock.fall(-1)
            break
    ground.update(rock)

def draw_solid(ground, highest):
    print()
    for y in range(highest, 0):
        print('% 3d\t|%s|'%(y,''.join(ROCK if (x,y) in ground else '.' for x in range(WID))))
    print('% 3d\t|%s|'%(0, '-'*WID))

def state_key(ground, rock_cycle, flow_cycle):
    key = ground.shape + [rock_cycle.key, flow_cycle.key]
    return tuple(key)

def main():
    rocks = parse_rocks()
    flows = tuple(1 if ch=='>' else -1 for ch in sys.stdin.read().strip())
    flow_cycle = CountCycle(flows)
    rock_cycle = CountCycle(rocks)
    ground = Ground()
    for _ in range(2022):
        rock_fall(next(rock_cycle), ground, flow_cycle)
    print("Part 1:", -ground.height)
    flow_cycle.reset()
    rock_cycle.reset()
    ground = Ground()
    states = {state_key(ground, rock_cycle, flow_cycle):(0,0)}
    turns = 0
    while True:
        rock_fall(next(rock_cycle), ground, flow_cycle)
        turns += 1
        key = state_key(ground, rock_cycle, flow_cycle)
        if key in states:
            break
        states[key] = (turns, ground.height)
    repeat_start = states[key]
    repeat_end = (turns, ground.height)
    repeat_turns = repeat_end[0] - repeat_start[0]
    repeat_height = repeat_end[1] - repeat_start[1]
    target = 1_000_000_000_000 # trillion
    repeats, remainder = divmod(target-repeat_start[0], repeat_turns)
    for _ in range(remainder):
        rock_fall(next(rock_cycle), ground, flow_cycle)
    remainder_height = ground.height - repeat_end[1]
    height = repeat_start[1] + repeat_height*repeats + remainder_height
    print("Part 2:", -height)

if __name__ == '__main__':
    main()
