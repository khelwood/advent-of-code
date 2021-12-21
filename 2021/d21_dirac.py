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
from collections import Counter, defaultdict
from typing import NamedTuple

ROLLS = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

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

class PlayState(NamedTuple):
    space_1: int
    space_2: int
    score_1: int=0
    score_2: int=0
    turn: int=0

def play_dirac(starts, all_rolls=ROLLS.items()):
    state = PlayState(*starts)
    win_counter = [0,0]
    score_states = defaultdict(Counter)
    score_states[0][state] = 1
    for score in range(41): # 40 is the max possible score without a winner
        state_counter = score_states[score]
        for state, count in state_counter.items():
            for roll, freq in all_rolls:
                st = next_state(state, roll)
                if st.score_1 >= 21:
                    win_counter[0] += count*freq
                elif st.score_2 >= 21:
                    win_counter[1] += count*freq
                else:
                    total_score = st.score_1 + st.score_2
                    score_states[total_score][st] += count*freq
        del score_states[score]
    return win_counter

def next_state(last, roll):
    turn = last.turn
    if turn==0:
        pos = (last.space_1 + roll - 1)%10 + 1
        score = last.score_1 + pos
        return PlayState(pos, last.space_2, score, last.score_2, 1)
    pos = (last.space_2 + roll - 1) % 10 + 1
    score = last.score_2 + pos
    return PlayState(last.space_1, pos, last.score_1, score, 0)


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

    w1,w2 = play_dirac(starts)
    if w1 > w2:
        print("Player 1 wins in", w1, "universes.")
    else:
        print("player 2 wins in", w2, "universes.")



if __name__ == '__main__':
    main()
