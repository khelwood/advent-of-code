#!/usr/bin/env python3

import sys

DEFAULT_DATA = '01000100010010111'
DEFAULT_SPACE = 272
# Part 2:
DEFAULT_SPACE = 35651584

def dragonise(a):
    b = ['1' if i=='0' else '0' for i in reversed(a)]
    return ''.join([a,'0']+b)
    
assert dragonise('111100001010')=='1111000010100101011110000'

def checksum_step(text, length):
    return ''.join('1' if text[i]==text[i+1] else '0'
                       for i in range(0,length,2))

def checksum(text, length=None):
    if length is None:
        length = len(text)
    while length%2==0:
        text = checksum_step(text, length)
        length = len(text)
    return text

def main(init_data, space):
    data = init_data
    while len(data) < space:
        data = dragonise(data)
    cs = checksum(data[:space])
    print("Checksum:",cs)
        
if __name__ == '__main__':
    data = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA
    space = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_SPACE
    main(data, space)
