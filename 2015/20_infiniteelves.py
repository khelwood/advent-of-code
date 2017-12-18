#!/usr/bin/env python3

"""The presents to house N are 10*(sum of all factors of N)."""

import sys
import itertools
import operator
from functools import reduce
from collections import namedtuple

Factitem = namedtuple('Factitem', 'factor index')

def _Factitem_values(self):
    p = 1
    f = self.factor
    yield p
    for _ in range(self.index):
        p *= f
        yield p

Factitem.values = _Factitem_values

def product(numbers):
    return reduce(operator.mul, numbers, 1)

def sum_factors(number):
    return product(sum(item.values()) for item in factorise(number))

def sum_factors_to_limit(number, limit):
    factors = list(factorise(number))
    min_fac = number//limit
    total = 0
    for combo in itertools.product(*(fac.values() for fac in factors)):
        prod = product(combo)
        if prod >= min_fac:
            total += prod
    return total

def factorise(number):
    if number%2==0:
        i = 1
        number//=2
        while number%2==0:
            i += 1
            number //= 2
        yield Factitem(2,i)
    prime = 3
    while prime*prime <= number:
        if number%prime==0:
            i = 1
            number //= prime
            while number%prime==0:
                i += 1
                number //= prime
            yield Factitem(prime, i)
        prime += 2
    if number > 1:
        yield Factitem(number,1)

def main(presents):
    house = 1
    np = 10
    print("10 presents to infinite houses")
    print(' ...', end='\r')
    while np < presents:
        house += 1
        np = 10*sum_factors(house)
    print("First house with %s presents: %s"%(np, house))
    np = 10
    limit = 50
    print("\n11 presents to 50 houses")
    print(' ...', end='\r')
    while np < presents:
        house += 1
        np = 11*sum_factors_to_limit(house, 50)
    print("First house with %s presents: %s"%(np, house))

if __name__ == '__main__':
    if len(sys.argv)!=2:
        exit("Usage: %s <number>"%sys.argv[0])
    main(int(sys.argv[1]))
