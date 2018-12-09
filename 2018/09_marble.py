#!/usr/bin/env python3

import sys
import re

class Game:
    def __init__(self, num_players, last_marble):
        self.scores = [0]*num_players
        self.last_marble = last_marble
        self.marbles = [0]
        self.cur_index = 0
        self.rounds = 0
    @property
    def num_players(self):
        return len(self.scores)
    @property
    def num_marbles(self):
        return len(self.marbles)
    @property
    def whose_turn(self):
        return self.rounds % self.num_players
    @property
    def next_marble(self):
        return self.rounds + 1
    @property
    def finished(self):
        return self.next_marble > self.last_marble
    def play_round(self):
        value = self.next_marble
        num_mar = self.num_marbles
        if value%23:
            pos = self.cur_index + 2
            if pos > num_mar:
                pos = 1
            self.marbles.insert(pos, value)
            self.cur_index = pos
        else:
            pi = self.whose_turn
            i = (self.cur_index - 7)%num_mar
            self.scores[pi] += value + self.marbles.pop(i)
            self.cur_index = i%num_mar
        self.rounds += 1
    def max_score(self):
        return max(self.scores)

def main():
    line = sys.stdin.read().strip()
    m = re.match(r'(\d+) players?; last marble is worth (\d+) points?', line)
    if not m:
        raise ValueError(repr(line))
    num_players, last_marble = map(int, m.groups())
    game = Game(num_players, last_marble)
    #game = Game(9, 25)
    while not game.finished:
        game.play_round()
    print("Winning score:", game.max_score())

if __name__ == '__main__':
    main()
