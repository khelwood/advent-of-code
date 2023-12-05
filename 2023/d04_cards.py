#!/usr/bin/env python3

import sys
import re

from typing import NamedTuple

NUM_PTN = re.compile(r'\d+')

class Card(NamedTuple):
    index:int
    win:set
    got:set

    def count_win(self):
        return len(self.got&self.win)

    def score(self):
        w = self.count_win()
        return w and (1<<(w-1))

def parse_card(line):
    i = line.index(':')
    j = line.rindex(' ', 0, i)+1
    index = int(line[j:i])
    line = line[i+1:]
    left, right = line.split('|')
    win = set(map(int, NUM_PTN.findall(left)))
    got = set(map(int, NUM_PTN.findall(right)))
    return Card(index, win, got)

def main():
    cards = [parse_card(line) for line in sys.stdin.read().splitlines()]
    score = sum(map(Card.score, cards))
    print("Part 1:", score)
    card_counts = {card.index:1 for card in cards}
    for card in cards:
        n = card_counts.get(card.index, 0)
        w = card.count_win()
        for i in range(1, w+1):
            card_counts[i+card.index] += n
    total_cards = sum(card_counts.values())
    print("Part 2:", total_cards)

if __name__ == '__main__':
    main()
