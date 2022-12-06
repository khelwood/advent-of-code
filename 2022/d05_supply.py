#!/usr/bin/env python3

import sys
import re

def read_stacks(lines):
    stacks = []
    for line in lines:
        line = line.rstrip()
        if not line:
            break
        n = (len(line) + 1)//4
        while len(stacks) < n:
            stacks.append([])
        for i in range(n):
            ch = line[4*i+1]
            if ch.isdigit():
                break
            if not ch.isspace():
                stacks[i].append(ch)
    for stack in stacks:
        stack.reverse()
    return stacks

def read_moves(lines):
    p = re.compile('move # from # to #$'.replace('#',r'(\d+)'))
    for line in lines:
        m = re.match(p, line)
        if m:
            yield tuple(map(int, m.groups()))

def apply_move(move, stacks, reverse:bool):
    num, src, dst = move
    source = stacks[src-1]
    payload = source[-num:]
    stacks[dst-1] += reversed(payload) if reverse else payload
    del source[-num:]

def main():
    stacks = read_stacks(sys.stdin)
    moves = list(read_moves(sys.stdin))
    stacks1 = [stack[:] for stack in stacks]
    for move in moves:
        apply_move(move, stacks1, reverse=True)
    print("Message:", ''.join(stack[-1] for stack in stacks1))
    for move in moves:
        apply_move(move, stacks, reverse=False)
    print("Message:", ''.join(stack[-1] for stack in stacks))


if __name__ == '__main__':
    main()
