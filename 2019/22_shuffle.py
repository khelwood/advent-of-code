#!/usr/bin/env python3

import sys
import re
from collections import namedtuple

Order = namedtuple('Order', 'function args')

ORDER_TYPES = []

def create_order(ptn):
    ptn = ptn.replace(' ', r'\s+').replace('#', '(-?[0-9]+)')
    ptn = re.compile(ptn, flags=re.I)
    def create_order(func):
        func.pattern = ptn
        ORDER_TYPES.append(func)
        return func
    return create_order

def parse_order(line):
    for order in ORDER_TYPES:
        m = re.match(order.pattern, line)
        if m:
            return Order(order, tuple(map(int, m.groups())))
    raise ValueError("Couldn't parse %r"%line)

@create_order('deal into new stack')
def perform_reverse(cards):
    return cards[::-1]

def position_reverse(num_cards, position):
    return (num_cards - 1 - position)

@create_order('cut #')
def perform_cut(cards, n):
    return cards[n:] + cards[:n]

def position_cut(num_cards, position, n):
    if n < 0:
        n += num_cards
    if position < n:
        return position + n
    return position - n

@create_order('deal with increment #')
def perform_deal(cards, n):
    pos = 0
    lc = len(cards)
    result = [None] * lc
    for card in cards:
        result[pos] = card
        pos = (pos+n)%lc
    return result

def position_deal(num_cards, position, n):
    # position = (n * value) % num_cards
    # derive value from position ...?
    TODO
    

def perform_orders(orders, cards):
    for order in orders:
        cards = order.function(cards, *order.args)
    return cards

def main():
    orders = tuple(map(parse_order, sys.stdin.read().strip().splitlines()))
    cards = perform_orders(orders, tuple(range(10007)))
    print("Card 2019 is at", cards.index(2019))

if __name__ == '__main__':
    main()
