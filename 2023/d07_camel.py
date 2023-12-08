#!/usr/bin/env python3

import sys
import re
from enum import Enum
from collections import Counter
from dataclasses import dataclass

LINE_PTN = re.compile(r'(\w+)\s+(\d+)')

VALUES = {str(c):c for c in range(2,10)}
VALUES.update(zip('TJQKA', range(10,15)))

class HandType(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE = 4
    FULL = 5
    FOUR = 6
    FIVE = 7

    def __lt__(self, other):
        return self.value < other.value


class Hand:
    def __init__(self, cards):
        self.cards = tuple(cards)
        self.type = handtype(self.cards)
    def __lt__(self, other):
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        return self.cards < other.cards
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, i):
        return self.cards[i]
    def __eq__(self, other):
        return self.type==other.type and self.cards==other.cards
    def make_wild(self):
        self.cards = tuple(1 if c==11 else c for c in self)
        self.type = wild_handtype(self.cards)


@dataclass
class HandBid:
    hand: Hand
    bid: int

    def __eq__(self, other):
        return self.hand==other.hand and self.bid==other.bid

    def __lt__(self, other):
        return self.hand < other.hand

    def make_wild(self):
        self.hand.make_wild()
        

def handtype(c):
    if not isinstance(c, Counter):
        c = Counter(c)
    cs = c.most_common(2)
    mc = cs[0][1]
    if mc==5:
        return HandType.FIVE
    if mc==4:
        return HandType.FOUR
    nc = cs[1][1]
    if mc==3:
        return HandType.FULL if nc==2 else HandType.THREE
    if mc==2:
        return HandType.TWO_PAIR if nc==2 else HandType.PAIR
    return HandType.HIGH_CARD

def wild_handtype(hand):
    c = Counter(hand)
    jv = 1
    jcount = c[jv]
    if jcount==0 or len(c)==1:
        return handtype(c)
    cs = c.most_common()
    mv,_ = cs[0]
    if mv==jv:
        mv,_ = cs[1]
    c[mv] += jcount
    c[jv] = 0
    return handtype(c)

def parse_hand(string):
    return Hand(VALUES[ch] for ch in string)


def parse_line(line):
    m = LINE_PTN.match(line)
    hand = parse_hand(m.group(1))
    bid = int(m.group(2))
    return HandBid(hand,bid)

def total_score(hbs):
    return sum(i*hb.bid for (i, hb) in enumerate(hbs, 1))

def main():
    hbs = list(map(parse_line, sys.stdin.read().splitlines()))
    hbs.sort()
    print("Part 1:", total_score(hbs))
    for hb in hbs:
        hb.make_wild()
    hbs.sort()
    print("Part 2:", total_score(hbs))

if __name__ == '__main__':
    main()
