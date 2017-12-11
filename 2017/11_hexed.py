#!/usr/bin/env python3

import sys

def desc(n, pos, neg):
    if n>0:
        return '%d %s'%(n, pos)
    if n<0:
        return '%d %s'%(-n, neg)
    return ''

def sign(n):
    return (1 if n>1 else -1 if n<0 else 0)

def apply_step(pos, direction, delta, alt1, delta1, alt2, delta2):
    if sign(pos[direction])==-delta:
        pos[direction] += delta
        return
    if sign(pos[alt1])==-delta1 or sign(pos[alt2])==-delta2:
        pos[alt1] += delta1
        pos[alt2] += delta2
        return
    pos[direction] += delta

def track_distance(split_data):
    loc = {'n': 0, 'nw': 0, 'ne': 0}
    most_steps = 0
    for d in split_data:
        if d=='n':
            apply_step(loc, 'n', 1, 'nw', 1, 'ne', 1)
        elif d=='s':
            apply_step(loc, 'n', -1, 'nw', -1, 'ne', -1)
        elif d=='ne':
            apply_step(loc, 'ne', 1, 'nw', -1, 'n', 1)
        elif d=='nw':
            apply_step(loc, 'nw', 1, 'ne', -1, 'n', 1)
        elif d=='se':
            apply_step(loc, 'nw', -1, 'ne', 1, 'n', -1)
        elif d=='sw':
            apply_step(loc, 'ne', -1, 'nw', 1, 'n', -1)
        else:
            raise ValueError(repr(d))
        steps = sum(map(abs, loc.values()))
        if steps > most_steps:
            most_steps = steps

    positions = [desc(loc[i], pos, neg) for (i, pos, neg) in 
                   (('n', "north", "south"),
                    ('nw', "northwest", "southeast"),
                    ('ne', "northeast", "southwest"))
                if loc[i]]
    print("Final position:", ', '.join(positions))
    print("Final distance:", steps)
    print("Greatest distance:", most_steps)
            
    
def main():
    data = sys.stdin.read()
    split_data = data.replace(',',' ').split()
    track_distance(split_data)

if __name__ == '__main__':
    main()
