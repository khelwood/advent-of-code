#!/usr/bin/env python3

import sys

def play_game(starting, limit):
    turn = 0
    memory = {}
    for x in starting:
        turn += 1
        memory[x] = turn
        gap = 0
    while turn < limit:
        turn += 1
        cur = gap
        previous = memory.get(cur)
        if previous is None:
            gap = 0
        else:
            gap = turn - previous
        memory[cur] = turn
    return cur

def main():
    starting = tuple(map(int, input().replace(',',' ').split()))
    print("2020th number is", play_game(starting, 2020))
    print("30000000th number is", play_game(starting, 30000000))

if __name__ == '__main__':
    main()
