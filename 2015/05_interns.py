#!/usr/bin/env python3

import sys
import re

THREE_VOWELS_PTN = re.compile('[aeiou].*[aeiou].*[aeiou]')
DOUBLE_LETTER_PTN = re.compile(r'([a-z])\1')
BANNED_PTN = re.compile('ab|cd|pq|xy')

def is_nice_v1(txt):
    return bool(THREE_VOWELS_PTN.search(txt) and DOUBLE_LETTER_PTN.search(txt)
            and not BANNED_PTN.search(txt))

REPEAT_PAIR_PTN = re.compile(r'([a-z]{2}).*\1')
REPEAT_SEPARATE_PTN = re.compile(r'([a-z]).\1')

def is_nice_v2(txt):
    return bool(REPEAT_PAIR_PTN.search(txt) and REPEAT_SEPARATE_PTN.search(txt))

def main():
    lines = sys.stdin.read().strip().split('\n')
    v1_count = sum(map(is_nice_v1, lines))
    print("Version 1 nice count:", v1_count)
    v2_count = sum(map(is_nice_v2, lines))
    print("Version 2 nice count:", v2_count)

if __name__ == '__main__':
    main()
