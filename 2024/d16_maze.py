#!/usr/bin/env python3

import sys

STEP_SCORE = 1
TURN_SCORE = 1000

class Point(tuple):
    @classmethod
    def at(cls, *args):
        return cls(args)
    def __add__(self, p):
        return Point(a+b for a,b in zip(self,p))
    def __sub__(self, p):
        return Point(a-b for a,b in zip(self,p))
    def __neg__(self):
        return Point(-a for a in self)
    def turn_left(self):
        return Point.at(self[1], -self[0])
    def turn_right(self):
        return Point.at(-self[1], self[0])

NORTH,EAST,SOUTH,WEST = map(Point, zip((0,1,0,-1), (-1,0,1,0)))
DIRS = (NORTH, EAST, SOUTH, WEST)

def read_maze():
    walls = set()
    for y,line in enumerate(filter(bool, map(str.strip, sys.stdin))):
        for x,ch in enumerate(line):
            if ch!='.':
                p = Point.at(x,y)
                if ch=='#':
                    walls.add(p)
                elif ch=='E':
                    end = p
                elif ch=='S':
                    start = p
    return walls, start, end

def next_step(walls, p, v):
    n = p+v
    if n not in walls:
        yield (n,v,STEP_SCORE)
    yield (p, v.turn_left(), TURN_SCORE)
    yield (p, v.turn_right(), TURN_SCORE)

def prev_step(walls, p, v):
    n = p-v
    if n not in walls:
        yield (n,v,STEP_SCORE)
    yield (p, v.turn_right(), TURN_SCORE)
    yield (p, v.turn_left(), TURN_SCORE)

def score_routes(walls, start, end):
    v = EAST
    new_states = [(start,v)]
    state_score = {(start,v):0}
    for p,v in new_states:
        score = state_score[p,v]
        for np, nv, ds in next_step(walls, p, v):
            state = (np,nv)
            prior = state_score.get(state)
            if prior is not None and prior <= score + ds:
                continue
            state_score[state] = score+ds
            new_states.append(state)
    return state_score

def best_seats(best_score, walls, state_score, start, end):
    states = set()
    new_states = {(end,v) for v in DIRS if state_score.get((end,v))==best_score}
    while new_states:
        cur_states = new_states
        new_states = set()
        for state in cur_states:
            if state in states:
                continue
            states.add(state)
            cur_score = state_score[state]
            p,v = state
            for np,nv,ds in prev_step(walls, p, v):
                if state_score[np,nv] + ds == cur_score:
                    new_states.add((np,nv))
    return {p for p,v in states}

def main():
    walls, start, end = read_maze()
    state_score = score_routes(walls, start, end)
    best_score = min(state_score[end,d] for d in DIRS if (end,d) in state_score)
    print(best_score)
    print(len(best_seats(best_score, walls, state_score, start, end)))

if __name__ == '__main__':
    main()
