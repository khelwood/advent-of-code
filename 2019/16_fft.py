#!/usr/bin/env python3

"""
Calculating the effect of the signal on a pattern
can be calculated using partial sums of the sequence.

The trick for part 2:
Observe that higher order patterns are simpler, because
they are bigger runs of 1s, 0s and -1s.
In fact, for the second half of the sequence, the
coefficients are all a sequence of zeroes followed by a sequence
of ones.
In fact, for the second half of the sequence,
all the signal digits to the left are irrelevant:
its next value is just the sum of itself and all the
later digits.
For instance, notice that the last digit of the signal never changes.
So as long as the offset puts is in the second half of the signal,
we only need the digits from there onwards, and the next phase
is made by summing up appropriate digits.
"""

import sys

def signal_part(signal, sums, order):
    ls = len(signal)
    if order==0:
        return abs(sum(signal[i] for i in range(0, ls, 4))
                -sum(signal[i] for i in range(2, ls, 4)))%10
    np = order + 1
    interval = 4*np
    last = ls-1
    total = sum(sums[min(i+2*order, last)] + sums[min(i+1+3*order, last)]
                - sums[min(i+order-1, last)] - sums[min(i+4*order+2, last)]
                for i in range(0, ls, interval))
    return abs(total)%10

def partial_sums(seq):
    total = 0
    sums = []
    for x in seq:
        total += x
        sums.append(total)
    return sums

def main():
    string = sys.stdin.read().strip()
    signal = tuple(map(int, string))
    ls = len(signal)
    for phase in range(100):
        sums = partial_sums(signal)
        signal = tuple(signal_part(signal, sums, i) for i in range(ls))
    print("Start of signal after 100 phases:", ''.join(map(str, signal[:8])))

    signal = tuple(map(int, string)) * 10_000
    offset = int(string[:7])
    print("\nOffset:", offset)
    assert offset >= len(signal)//2
    signal = list(signal[offset:])
    ls = len(signal)
    for phase in range(100):
        total = 0
        for i in range(ls-1, -1, -1):
            signal[i] = total = (total + signal[i])%10
    print('Message:', ''.join(map(str, signal[:8])))

if __name__ == '__main__':
    main()
