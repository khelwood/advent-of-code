#!/usr/bin/env python3

import sys

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
    if len(sys.argv) <= 1:
        exit("Usage: %s <input>"%sys.argv[0])
    data = sys.argv[1]
    for space in [272, 35651584]:
        print("Space:", space)
        print(" ... ", end='\r')
        main(data, space)
