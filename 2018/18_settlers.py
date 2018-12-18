#!/usr/bin/env python3

import sys
import itertools

OPEN = '.'
TREE = '|'
YARD = '#'

ADJACENT = ((-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1))

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def count_adj(p, units, dirs=ADJACENT):
    return sum((addp(p, d) in units) for d in dirs)

def any_adj(p, units, dirs=ADJACENT):
    return any((addp(p,d) in units) for d in dirs)

def next_state(yards, trees):
    new_yards = set()
    removed_yards = set()
    new_trees = set()
    for pos in itertools.product(range(WIDTH), range(HEIGHT)):
        if pos in trees:
            if count_adj(pos, yards)>=3:
                new_yards.add(pos)
        elif pos in yards:
            if not (any_adj(pos, trees) and any_adj(pos, yards)):
                removed_yards.add(pos)
        else:
            if count_adj(pos, trees)>=3:
                new_trees.add(pos)
    yards = yards - removed_yards | new_yards
    trees = trees - new_yards | new_trees
    return yards, trees

def read_state():
    global WIDTH, HEIGHT
    yards = set()
    trees = set()
    for y,line in enumerate(sys.stdin):
        for x,value in enumerate(line.strip()):
            if value==TREE:
                trees.add((x,y))
            elif value==YARD:
                yards.add((x,y))
    WIDTH = x+1
    HEIGHT = y+1
    return frozenset(yards), frozenset(trees)

def display(yards, trees):
    symbol = lambda p: TREE if p in trees else YARD if p in yards else OPEN
    for y in range(HEIGHT):
        print(''.join([symbol((x,y)) for x in range(WIDTH)]))

def main():
    first_target = 10
    second_target = 10**9
    st = read_state()
    states = [st]
    state_index = {st:0}

    for i in range(first_target):
        st = next_state(*st)
        states.append(st)
        state_index[st] = i
    yards, trees = st
    print("First result:", len(yards)*len(trees))

    repeat_start = None
    repeat_end = None
    for i in range(first_target, second_target):
        st = next_state(*st)
        if st in state_index:
            repeat_start = state_index[st]
            repeat_end = i
            break
        state_index[st] = i
        states.append(st)
    print(f"(Pattern repeats between {repeat_start} and {repeat_end})")
    if repeat_end:
        period = repeat_end - repeat_start
        index = repeat_start + (second_target - repeat_start) % period
        yards, trees = states[index]
    else:
        yards, trees = st
    print("Final result:", len(yards)*len(trees))

if __name__ == '__main__':
    main()
