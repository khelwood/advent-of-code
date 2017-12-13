#!/usr/bin/env python3

import sys
import hashlib

def find_hashes(door):
    i = 0
    while True:
        i += 1
        h = make_hash(door, i)
        if hash_ok(h):
            yield h

def first_password(door, length=8):
    results = []
    i = 0
    for h in find_hashes(door):
        results.append(h[5])
        if len(results) >= length:
            break
    return ''.join(results)

def second_password(door, length=8):
    results = ['.']*length
    found = 0
    for h in find_hashes(door):
        i = ord(h[5])-ord('0')
        if 0<=i<length and results[i]=='.':
            results[i] = h[6]
            print('  %s'%(''.join(results)), end='\r')
            found += 1
            if found >= length:
                break
    return ''.join(results)

def make_hash(door, i):
    s = door+str(i)
    return hashlib.md5(s.encode('ascii')).hexdigest()

def hash_ok(h):
    return h.startswith('00000')

def main():
    if len(sys.argv) <= 1:
        exit("Usage: %s <doorid>"%sys.argv[0])
    door = sys.argv[1]
    print("Door id:", door)
    print(" Working",end='\r')
    pw = first_password(door)
    print("First password:", pw)
    print(" Working",end='\r')
    pw = second_password(door)
    print("Second password:", pw)

if __name__ == '__main__':
    main()
