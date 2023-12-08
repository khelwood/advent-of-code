#!/usr/bin/env python3

import sys
import re
from enum import Enum
from collections import Counter

LINE_PTN = re.compile(r'(\w+)\s+(\d+)')

VALUES = {str(c):c for c in range(2,10)}
VALUES.update(zip('TJQKA', range(10,15)))
WILDCARD = 1

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
    def __init__(self, cards, bid):
        self.cards = tuple(cards)
        self.type = handtype(self.cards)
        self.bid = bid

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

    def make_wild(self):
        self.cards = tuple(WILDCARD if c==11 else c for c in self)
        self.type = handtype(self.cards)
        

def handtype(cards):
    c = Counter(cards)
    jcount = c[WILDCARD]
    if jcount > 0 and len(c) > 1:
        cs = c.most_common(2)
        mv,_ = cs[0]
        if mv==WILDCARD:
            mv,_ = cs[1]
        c[mv] += jcount
        c[WILDCARD] = 0
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

def parse_hand(line):
    m = LINE_PTN.match(line)
    return Hand((VALUES[ch] for ch in m.group(1)), int(m.group(2)))

def total_score(hands):
    return sum(i*hand.bid for (i, hand) in enumerate(hands, 1))

def main():
    hands = list(map(parse_hand, sys.stdin.read().splitlines()))
    hands.sort()
    print("Part 1:", total_score(hands))
    for hand in hands:
        hand.make_wild()
    hands.sort()
    print("Part 2:", total_score(hands))

if __name__ == '__main__':
    main()
