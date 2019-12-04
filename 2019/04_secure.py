#!/usr/bin/env python3

import sys

def count_matches(mn, mx, func):
    return sum(func(c) for c in range(mn, mx+1))

def simple_pw(num):
    string = str(num)
    rep = False
    for i in range(1, len(string)):
        if string[i]==string[i-1]:
            rep = True
        elif string[i] < string[i-1]:
            return False
    return rep

def complex_pw(num):
    string = str(num)
    rep = False
    ls = len(string)
    for i in range(1, ls):
        if string[i]==string[i-1]:
            if ((i<2 or string[i-2]!=string[i])
                    and (i + 1 == ls or string[i+1]!=string[i])):
                rep = True
        elif string[i] < string[i-1]:
            return False
    return rep

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
