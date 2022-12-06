#!/usr/bin/env python3

import sys

INPUT_DICT = {
    'A':'R', 'X':'R',
    'B':'P', 'Y':'P',
    'C':'S', 'Z':'S',
}

BEATS = { 'R':'S', 'S':'P', 'P':'R' }
LOSES_TO = {y:x for (x,y) in BEATS.items()}

CHOICE_SCORE = {k:i for (i,k) in enumerate('RPS', 1)}

def select_choice(x,y):
    match y:
        case 'X': return BEATS[x]
        case 'Y': return x
        case 'Z': return LOSES_TO[x]

def read_input():
    return [line.split() for line in filter(bool, map(str.strip, sys.stdin))]

def parse(data, dictionary):
    return [tuple(dictionary[x] for x in line) for line in data]

def parse_strategy(data):
    return [parse_line_strategy(*line) for line in data]

def parse_line_strategy(x,y):
    x = INPUT_DICT[x]
    y = select_choice(x,y)
    return (x,y)

def score_round(x,y):
    if x==y:
        return 3
    return 6 if BEATS[y]==x else 0

def score(data):
    return sum(CHOICE_SCORE[y] + score_round(x,y) for (x,y) in data)

def main():
    data = read_input()
    parsed = parse(data, INPUT_DICT)
    print("Score:", score(parsed))
    parsed = parse_strategy(data)
    print("Score:", score(parsed))


if __name__ == '__main__':
    main()
