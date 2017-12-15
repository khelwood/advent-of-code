#!/usr/bin/env python3

import sys
import hashlib

def number_hash(text):
    return hashlib.md5(text.encode('ascii')).hexdigest()

def match_hash(key, prefix, start=1):
    i = start
    while True:
        h = number_hash(key+str(i))
        if h.startswith(prefix):
            return i
        i += 1

def main():
    if len(sys.argv)!=2:
        exit("Usage: %s <key>"%sys.argv[0])
    key = sys.argv[1]
    n1 = match_hash(key, '00000')
    print("Lowest number (five zeroes):", n1)
    n2 = match_hash(key, '000000', n1)
    print("Lowest number (six zeroes):", n2)
    
if __name__ == '__main__':
    main()
