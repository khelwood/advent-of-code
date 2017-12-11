#!/usr/bin/env python3

import sys

def cull(num_elfs):
    elfs = list(range(1, num_elfs+1, 2))
    i = (elfs[-1]==num_elfs)
    while len(elfs) > 1:
        last = elfs[-1]
        elfs = elfs[i::2]
        i = (elfs[-1]==last)
    return elfs[0]

def explicit_steal(elfs, pos):
    num_left = num_elfs
    num_removed = 0
    o = pos + len(elfs)//2 + num_removed//2
    elfs[o] = None

def contract(seq):
    return [x for x in seq if x]
    
def steal_opposite(num_elfs):
    elfs = list(range(1, num_elfs+1))
    num_left = num_elfs
    while num_left > 1:
        i = 0
        num_removed = 0
        L = len(elfs)
        # Null out entries until we reach a point where
        #  it would affect our calculations.
        while elfs[i] and num_left > 1:
            o = (i + (L+num_removed)//2)%L
            elfs[o] = None
            #print(f"Elf {elfs[i]} steals from elf {elfs[o]}")
            #print(contract(elfs))
            num_left -= 1
            num_removed += 1
            i += 1
        print(" num_left: %r   "%num_left, end='\r')
        # Then contract spaces, putting the current position
        #  at the start of the new list for convenience.
        elfs = contract(elfs[i+1:]) + contract(elfs[:i])
    return elfs[0]

def main(num):
    print('Part 1 result:', cull(num))
    r = steal_opposite(num)
    print('Part 2 result:', r) # lower than 1468247

if __name__ == '__main__':
    main(int(sys.argv[1]))
