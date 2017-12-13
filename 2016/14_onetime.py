#!/usr/bin/env python3

import sys
import re
import hashlib

def enumerate_hashes(salt, reps, start=0, stop=None):
    index = start
    while index!=stop:
        h = get_hash(salt, index, reps)
        yield (index, h)
        index += 1

def get_hash(salt, index, reps, caches={}):
    cache = caches.get(reps)
    if cache is None:
        cache = []
        caches[reps] = cache
    while len(cache) <= index:
        cache.append(make_hash(salt+str(len(cache)), reps))
    return cache[index]

def make_hash(text, reps):
    for _ in range(reps):
        text = hashlib.md5(text.encode('ascii')).hexdigest()
    return text
    
def find_keys(salt, reps, ptn=re.compile(r'(.)\1\1')):
    for i,h in enumerate_hashes(salt, reps):
        m = ptn.search(h)
        if m:
            k = m.group(1)
            sought = k*5
            if any(sought in v
                  for _,v in enumerate_hashes(salt, reps, i+1, i+1001)):
                yield i


def print_keys(salt, reps):
    i = 0
    for k in find_keys(salt, reps):
        print(k, end=' ', flush=True)
        i += 1
        if i>= 64:
            return k 

def main():
    if len(sys.argv)<=1:
        exit("Usage: %s <salt>"%sys.argv[0])
    salt = sys.argv[1]
    print("Part 1: ...")
    k1 = print_keys(salt, 1)
    print("\nPart 2: ...")
    k2 = print_keys(salt, 2017)
    print("\n\nPart 1 result:", k1)
    print("Part 2 result:", k2)
    

if __name__ == '__main__':
    main()
