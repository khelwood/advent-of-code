#!/usr/bin/env python3

import sys
import re

from collections import defaultdict

MONSTER = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''.lstrip('\n').rstrip()

class Tile:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.match = None
    @property
    def top_link(self):
        lk = self.match
        return lk and lk.flipped
    @property
    def right_link(self):
        lk = self.rot_left.top_link
        return lk and lk.rot_right
    @property
    def left_link(self):
        lk = self.rot_right.top_link
        return lk and lk.rot_left
    @property
    def bottom_link(self):
        lk = self.rot_180.top_link
        return lk and lk.rot_180

def find(seq, value, start=0, end=None):
    if end is None:
        end = len(seq)
    for i in range(start, end):
        if seq[i]==value:
            return i
    return -1

def splitlist(lines, value):
    j=0
    while (i:=find(lines, value, j+1)) >= 0:
        yield lines[j:i]
        j = i+1
    if j < len(lines):
        yield lines[j:]

def rotate_clockwise(lines):
    wid = len(lines)
    return [
        ''.join([lines[wid-1-x][y] for x in range(wid)])
        for y in range(wid)
    ]

def make_tiles(tile_id, data):
    original_data = data
    tiles = [Tile(tile_id, data)]
    for _ in range(3):
        data = rotate_clockwise(data)
        tiles.append(Tile(tile_id, data))
    for i,tile in enumerate(tiles):
        tile.rot_left = tiles[i-1]
        tile.rot_180 = tiles[i-2]
        tile.rot_right = tiles[i-3]
        tile.flipped = Tile(tile_id, list(reversed(tile.data)))
        tile.flipped.flipped = tile
    for tile in tiles:
        tile.flipped.rot_left = tile.rot_right.flipped
        tile.flipped.rot_right = tile.rot_left.flipped
        tile.flipped.rot_180 = tile.rot_180.flipped
    tiles += [tile.flipped for tile in tiles]
    return tiles


def read_tiles(lines):
    for block in splitlist(lines, ''):
        tile_id = int(re.match(r'Tile (\d+):', block[0]).group(1))
        data = block[1:]
        yield from make_tiles(tile_id, data)

def link_tiles(tiles):
    tops = defaultdict(set)
    for tile in tiles:
        edge = tile.data[0]
        tops[edge].add(tile)
    for v in tops.values():
        if len(v) < 2:
            continue
        if len(v) > 2:
            raise ValueError(f"Ambiguous jigsaw edge detected: {v}")
        a,b = v
        a.match = b
        b.match = a

def product(values):
    n = 1
    for v in values:
        n *= v
    return n

def assemble(tiles, start, WID=12):
    grid = {}
    grid[0,0] = start
    last = start
    for y in range(WID):
        if y > 0:
            above = grid[0,y-1]
            last = grid[0,y-1].bottom_link
            grid[0,y] = last
        for x in range(1, WID):
            last = last.right_link
            grid[x,y] = last
    return grid


def render(grid):
    tile = grid[0,0]
    tile_w = len(tile.data[0]) - 2 # omit tile edges
    megagrid = {}
    for (gx,gy),tile in grid.items():
        x0 = gx*tile_w
        y0 = gy*tile_w
        for y in range(tile_w):
            line = tile.data[y+1]
            for x in range(tile_w):
                ch = line[x+1]
                megagrid[x0+x, y0+y] = ch
    return megagrid

def monster_orientations(x0, y0, monster, top):
    basic = [(x0+x,y0+y) for (x,y) in monster]
    for _ in range(2):
        yield basic
        yield [(top-x, y) for (x,y) in basic]
        yield [(x, top-y) for (x,y) in basic]
        yield [(top-x, top-y) for (x,y) in basic]
        basic = [(y,x) for (x,y) in basic]

def find_monsters(grid):
    monster = {(x,y) for y,line in enumerate(MONSTER.splitlines())
                    for x,ch in enumerate(line) if ch=='#'}
    xmax = max(x for (x,y) in monster)
    ymax = max(y for (x,y) in monster)
    SIZE = max(x for (x,y) in grid)
    monsters = 0
    for y0 in range(SIZE-ymax):
        for x0 in range(SIZE-xmax):
            for smo in monster_orientations(x0,y0, monster, SIZE-1):
                if all(grid[p]!='.' for p in smo):
                    monsters += 1
                    for p in smo:
                        grid[p]='O'
    return monsters

def main():
    tiles = list(read_tiles(sys.stdin.read().splitlines()))

    link_tiles(tiles)
    corners = [tile for tile in tiles
                if tile.top_link is None and tile.left_link is None]
    print("Product of corners:", product({tile.id for tile in corners}))

    grid = assemble(tiles, corners[0])
    megagrid = render(grid)
    print("Found",find_monsters(megagrid),"monsters.")
    hashes = sum(v=='#' for v in megagrid.values())
    print("Extraneous hashes:", hashes)


if __name__ == '__main__':
    main()
