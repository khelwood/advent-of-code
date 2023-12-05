#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

PTN = re.compile(r'\s*(\d+)\s+(\w+)')

COLOURS = ('red', 'green', 'blue')

Game = namedtuple('Game', 'index rounds')

def parse_game(line):
    i = line.index(':')
    j = line.rindex(' ', 0, i)+1
    index = int(line[j:i])
    line = line[i+1:]
    parts = line.split(';')
    rounds = []
    for part in parts:
        r = {}
        for n,c in re.findall(PTN, part):
            r[c] = int(n)
        rounds.append(r)
    return Game(index, rounds)

def round_valid(rnd, total):
    return all(n <= total[c] for (c,n) in rnd.items())

def game_valid(game, total):
    return all(round_valid(rnd, total) for rnd in game.rounds)

def min_cubes(game):
    return {c:max(rnd.get(c, 0) for rnd in game.rounds) for c in COLOURS}

def cube_power(cubes):
    p = 1
    for v in cubes.values():
        p *= v
    return p

def main():
    games = list(map(parse_game, sys.stdin.read().splitlines()))
    total = {'red':12, 'green':13, 'blue':14}
    score = sum(game.index for game in games if game_valid(game, total))
    print("Part 1:", score)
    score = sum(cube_power(min_cubes(game)) for game in games)
    print("Part 2:", score)

if __name__ == '__main__':
    main()
