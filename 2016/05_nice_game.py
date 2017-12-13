#!/usr/bin/env python3

import sys
import hashlib

def make_hash(door, i):
    s = door+str(i)
    return hashlib.md5(s.encode('ascii')).hexdigest()

def hash_ok(h):
    return h.startswith('00000')

_next_hash = 0

def find_hashes(door, cached_hashes=[]):
    global _next_hash
    yield from cached_hashes
    while True:
        h = make_hash(door, _next_hash)
        _next_hash += 1
        if hash_ok(h):
            cached_hashes.append(h)
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
