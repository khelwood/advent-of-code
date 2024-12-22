#!/usr/bin/env python3

import sys
from collections import Counter

PRUNE_MASK = (1<<24)-1

def next_secret(n):
    n ^= (n*64)
    n &= PRUNE_MASK
    n ^= (n//32)
    n &= PRUNE_MASK
    n ^= (n*2048)
    n &= PRUNE_MASK
    return n

def ith_secret(n, i):
    for _ in range(i):
        n = next_secret(n)
    return n

def find_prices(n, i):
    prices = [n%10]
    changes = [None]
    for _ in range(i):
        n = next_secret(n)
        price = n%10
        changes.append(price - prices[-1])
        prices.append(price)
    return tuple(prices), tuple(changes)

def main():
    ns = list(map(int, sys.stdin.read().split()))
    print(sum(ith_secret(n, 2000) for n in ns))
    seqs = [find_prices(n, 2000) for n in ns]
    c = Counter()
    for prices, changes in seqs:
        done = set()
        for i in range(4, len(changes)):
            key = changes[i-3:i+1]
            if key not in done:
                c[key] += prices[i]
                done.add(key)
    print(c.most_common()[0])

if __name__ == '__main__':
    main()
