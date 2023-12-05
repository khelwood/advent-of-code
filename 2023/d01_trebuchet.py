#!/usr/bin/env python3

import sys

def calibration_1(string):
    digits = [ch for ch in string if ch.isdigit()]
    return int(digits[0] + digits[-1])

word_numbers = 'zero one two three four five six seven eight nine'.split()
word_numbers = {w:str(n) for n,w in enumerate(word_numbers)}

def word_sub(m):
    return word_numbers[m.group()]

def first_digit(string):
    for i,ch in enumerate(string):
        if ch.isdigit():
            return ch
        w = next((w for w in word_numbers if string.startswith(w, i)), None)
        if w:
            return word_numbers[w]

def last_digit(string):
    w = next((w for w in word_numbers if string.endswith(w)), None)
    if w:
        return word_numbers[w]
    for i in range(len(string)-1, -1, -1):
        if string[i].isdigit():
            return string[i]
        w = next((w for w in word_numbers if string.endswith(w, 0, i)), None)
        if w:
            return word_numbers[w]

def calibration_2(string):
    return int(first_digit(string) + last_digit(string))

def main():
    data = list(filter(bool, sys.stdin.read().splitlines()))
    v1 = sum(map(calibration_1, data))
    print("Calibration sum 1:", v1)
    v2 = sum(map(calibration_2, data))
    print("Calibration sum 2:", v2)

    

if __name__ == '__main__':
    main()
