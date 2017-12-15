#!/usr/bin/env python3

import sys

def index_of_floor(code, floor):
    cur = 0
    for i,ch in enumerate(code, 1):
        cur += 1 if ch=='(' else -1
        if cur==floor:
            return i

def main():
    code = sys.stdin.read().strip()
    floor = code.count('(') - code.count(')') # or len(code)-2*code.count(')')
    print("End floor", floor)
    index = index_of_floor(code, -1)
    print("Index of basement", index)
    

if __name__ == '__main__':
    main()
