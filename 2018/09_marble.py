#!/usr/bin/env python3

import sys
import re

class Marble:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
    def drop(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        self.next = None
        self.prev = None
    def insert(self, m):
        m.next = self.next
        m.next.prev = m
        m.prev = self
        self.next = m

class Game:
    def __init__(self, num_players, last_value):
        self.scores = [0]*num_players
        self.last_value = last_value
        m = Marble(0)
        self.current = m.next = m.prev = m
        self.rounds = 0
        self.orig = m
    @property
    def num_players(self):
        return len(self.scores)
    @property
    def whose_turn(self):
        return self.rounds % self.num_players
    @property
    def next_value(self):
        return self.rounds + 1
    @property
    def finished(self):
        return self.next_value > self.last_value
    def play_round(self):
        value = self.next_value
        if value % 23:
            m = Marble(value)
            self.current.next.insert(m)
            self.current = m
        else:
            pi = self.whose_turn
            m = self.current.prev.prev.prev.prev.prev.prev.prev
            self.scores[pi] += value + m.value
            self.current = m.next
            m.drop()
        self.rounds += 1
    def max_score(self):
        return max(self.scores)
    def desc(self):
        print(f"{self.rounds} [{self.whose_turn}] ", end='')
        c = self.orig
        while True:
            if c==self.current:
                print(f"({c.value})".ljust(4), end='')
            else:
                print(f"{c.value}".ljust(4), end='')
            c = c.next
            if c==self.orig:
                break
        print()

def main():
    line = sys.stdin.read().strip()
    m = re.match(r'\D*(\d+)\D+(\d+)\D', line)
    if not m:
        raise ValueError(repr(line))
    num_players, last_marble = map(int, m.groups())
    game = Game(num_players, last_marble)
    while not game.finished:
        game.play_round()
    print("Winning score:", game.max_score())
    game = Game(num_players, last_marble*100)
    while not game.finished:
        game.play_round()
    print("Winnig score:", game.max_score())

if __name__ == '__main__':
    main()
