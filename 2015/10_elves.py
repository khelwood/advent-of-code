#!/usr/bin/env python3

import sys

def iter_similar(sequence):
    last = None
    for n in sequence:
        if n==last:
            size += 1
        else:
            if last is not None:
                yield last
                yield size

def looksay_once(numbers):
    result = []
    last = None
    size = 0
    for n in numbers:
        if n==last:
            size += 1
        else:
            if last is not None:
                result.append(str(size))
                result.append(last)
            last = n
            size = 1
    if size > 0:
        result.append(str(size))
        result.append(last)
    return ''.join(result)


def looksay(numbers, times):
    for _ in range(times):
        numbers = looksay_once(numbers)
    return numbers

def main(start):
    print("Start:", start)
    for n in (40,50):
        print("After %s turns:"%n)
        print(' ...', end='\r')
        result = looksay(start, n)
        if len(result)<60:
            print("Result:", result)
        print("Result length:", len(result))
    
if __name__ == '__main__':
    if len(sys.argv)!=2:
        exit("Usage: %s <number>"%sys.argv[0])
    main(sys.argv[1])
