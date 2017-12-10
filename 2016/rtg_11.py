#!/usr/bin/env python3

from itertools import combinations

PART = 2

START='00010102222'
COLUMNS = 'E T TG P PG S SG M MG R RG'

if PART==2:
    START += '0000'
    COLUMNS += 'L LG D DG'

START = tuple(ord(ch)-ord('0') for ch in START)
COLUMNS = tuple(x.ljust(2) for x in COLUMNS.split())


def presence(seq, floor, ci):
    return COLUMNS[ci] if seq[ci]==floor else '. '

def describe(seq):
    for floor in range(3, -1, -1):
        presences = [presence(seq, floor, ci) for ci in range(len(COLUMNS))]
        print(f'F{floor+1}  {" ".join(presences)}')

cur_states = [START]
seen = {START}
next_states = []

def find_moves(cur):
    cur = list(cur)
    yield from find_up_moves(cur)
    yield from find_down_moves(cur)

def find_up_moves(cur):
    if cur[0]==3:
        return
    new_floor = cur[0]+1
    for inv in find_invs(cur):
        x = list(cur)
        x[0] = new_floor
        for i in inv:
            x[i] = new_floor
        yield x
    
def find_down_moves(cur):
    if cur[0]==0 or cur[0]==min(cur):
        return
    new_floor = cur[0]-1
    for inv in find_invs(cur):
        # This is the bit that makes it much faster:
        #  Never take any chip downwards.
        #  (I have a proof for this but it too long
        #  to write in the margin.)
        if any(i%2 for i in inv):
            continue
        x = list(cur)
        x[0] = new_floor
        for i in inv:
            x[i] = new_floor
        yield x


def legal(state):
    lonely_chip_floors = set()
    gen_floors = set()
    for i in range(1, len(state), 2):
        if state[i]!=state[i+1]:
            lonely_chip_floors.add(state[i])
        gen_floors.add(state[i+1])
    return not (gen_floors & lonely_chip_floors)
            
def is_win(state):
    return all(x==3 for x in state)

def find_invs(cur):
    N = len(cur)
    floor = cur[0]
    invs = [i for i in range(1,N) if cur[i]==floor]
    yield from combinations(invs, 1)
    yield from combinations(invs, 2)

def find_next_moves():
    for cur in cur_states:
        for ns in find_moves(cur):
            if is_win(ns):
                return True
            if not legal(ns):
                continue
            ns = tuple(ns)
            if ns not in seen:
                next_states.append(ns)
                seen.add(ns)

def main():
    global cur_states
    global next_states
    describe(START)
    moves = 1
    while not find_next_moves():
        moves += 1
        print(f' (move {moves}, checked {len(seen)})',end='\r')
        cur_states = next_states
        next_states = []
    print(f"Moves: {moves}                         ")
        
if __name__ == '__main__':
    main()
