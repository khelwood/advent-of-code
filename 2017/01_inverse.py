#!/usr/bin/env python3

import sys

def reverse_captcha(data, offset):
    return sum(num if num==data[i-offset] else 0 for i,num in enumerate(data))

def main():
    data = [int (n) for n in sys.stdin.read().strip()]
    num = reverse_captcha(data, 1)
    print("Part 1:", num)
    num = reverse_captcha(data, len(data)//2)
    print("Part 2:", num)

if __name__ == '__main__':
    main()
