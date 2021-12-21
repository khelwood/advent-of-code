#!/usr/bin/env python3

"""
Spaces are numbered 1 to 10 on a circular track.
Each of two players has a starting space.
Per turn, each player rolls three dice and moves forward around the track.
Score is increased by the number of the space they land on.
Target score is 1000.
Die rolls 1 then 2 then 3 ... 100, then 1 then 2 ...
"""

import sys
from itertools import cycle
from dataclasses import dataclass

@dataclass
class Player:
    space:int
    score:int = 0
    def advance(self, amount):
        self.space = (self.space + amount - 1)%10 + 1
        self.score += self.space

def play_to_end(players, die):
    die_rolls = 0
    while True:
        for pl in players:
            progress = next(die) + next(die) + next(die)
            die_rolls += 3
            pl.advance(progress)
            if pl.score >= 1000:
                return die_rolls

def main():
    if len(sys.argv) != 3:
        exit(f"Usage: {sys.argv[0]} <start1> <start2>")
    starts = (int(sys.argv[1]), int(sys.argv[2]))
    players = tuple(map(Player, starts))
    die_rolls = play_to_end(players, cycle(range(1,101)))
    print("Die rolls:", die_rolls)
    losing_score = min(pl.score for pl in players)
    print("Losing score:", losing_score)
    print("Result:", die_rolls * losing_score)


if __name__ == '__main__':
    main()
