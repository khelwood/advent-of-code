#!/usr/bin/env python3

import sys

def count_matches(mn, mx, func):
    c = skip_to_monotonic(mn)
    n = 0
    while c <= mx:
        if func(c):
            n += 1
        c += 1
        if c%10==0:
            c = skip_to_monotonic(c)
    return n

def skip_to_monotonic(c):
    numbers = list(str(c))
    for i in range(1, len(numbers)):
        if numbers[i] < numbers[i-1]:
            numbers[i] = numbers[i-1]
    return int(''.join(numbers))

def simple_pw(num):
    string = str(num)
    return any(string[i]==string[i-1] for i in range(1, len(string)))

def complex_pw(num):
    string = str(num)
    ls = len(string)
    for i in range(1, ls):
        if (string[i]==string[i-1]
                and (i<2 or string[i-2]!=string[i])
                and (i + 1 == ls or string[i+1]!=string[i])):
            return True
    return False

def main():
    line = input("Puzzle input: ")
    mn, mx = map(int, line.split('-'))
    print(mn,"to",mx)
    ns = count_matches(mn,mx, simple_pw)
    print("Part 1:", ns)
    nc = count_matches(mn,mx, complex_pw)
    print("Part 2:", nc)

if __name__ == '__main__':
    main()
