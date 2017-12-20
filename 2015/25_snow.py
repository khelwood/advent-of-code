#!/usr/bin/env python3

import sys

def item_index(row, col):
    diagonal = row+col-1
    triangle = diagonal*(diagonal+1)//2
    return triangle-row

def sequence_item(row, col, start, multiplier, divisor):
    i = item_index(row, col)
    mul = power_mod(multiplier, i, divisor)
    return (start*mul)%divisor

def power_mod(a, b, c):
    """(A**B)%C can be calculated as
    the product of (A**p)%C where each p is a power of two
    from B's binary expansion.
    (A**p)%C can be iteratively worked out by letting
    A=(A*A)%C for each further power of two."""
    a %= c
    p = 1
    for bit in bin(b)[::-1]:
        if bit=='1':
            p = (p*a)%c
        a = (a*a)%c
    return p

def main():
    if len(sys.argv)!=3:
        exit("Usage: %s <row> <col>"%sys.argv[0])
    row = int(sys.argv[1])
    col = int(sys.argv[2])

    START = 20151125
    MULTIPLIER = 252533
    DIVISOR = 33554393
    print(sequence_item(row, col, START, MULTIPLIER, DIVISOR))

if __name__ == '__main__':
    main()
