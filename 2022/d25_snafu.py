#!/usr/bin/env python3

import sys

SNAFU_DIGITS = {ch:i for i,ch in enumerate('=-012', -2)}
DIGIT_SNAFU = {v:k for (k,v) in SNAFU_DIGITS.items()}

def to_snafu(n):
    digits = []
    while n:
        v = n%5
        if v <= 2:
            digits.append(DIGIT_SNAFU[v])
        else:
            digits.append(DIGIT_SNAFU[v-5])
            n += 5
        n //= 5
    return ''.join(reversed(digits))

def parse_snafu(s):
    total = 0
    for ch in s:
        total = 5*total + SNAFU_DIGITS[ch]
    return total

def main():
    total = sum(parse_snafu(line.strip()) for line in sys.stdin)
    print(to_snafu(total))

if __name__ == '__main__':
    main()
