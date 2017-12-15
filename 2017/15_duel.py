#!/usr/bin/env python3

import sys

class Generator:
    def __init__(self, factor, divisor, start, filter_number=None):
        self.factor = factor
        self.divisor = divisor
        self.start = start
        self.filter_number = filter_number
    def __iter__(self):
        value, factor, divisor = self.start, self.factor, self.divisor
        filter_number = self.filter_number
        while True:
            value = (value * factor) % divisor
            if filter_number is None or value%filter_number==0:
                yield value

def count_matches(generators, limit):
    gen_iters = zip(*generators)
    count = 0
    mask = (1<<16)-1
    next_print = 0
    print_delta = limit // 100
    for i in range(limit):
        n1, n2 = next(gen_iters)
        if (n1&mask)==(n2&mask):
            count += 1
        if i>=next_print:
            print(" %s"%i, end='\r')
            next_print += print_delta
    return count

def main():
    if len(sys.argv)!=3:
        exit("Usage: %s <num> <num>"%sys.argv[0])
    starts = [int(n) for n in sys.argv[1:]]
    factors = [16807, 48271]
    divisor = 2147483647
    generators = [Generator(f, divisor, v) for (f,v) in zip(factors, starts)]
    n = count_matches(generators, 40_000_000)
    print("Part 1 count:", n)
    generators[0].filter_number = 4
    generators[1].filter_number = 8
    n = count_matches(generators, 5_000_000)
    print("Part 2 count:", n)

if __name__ == '__main__':
    main()
