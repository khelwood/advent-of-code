#!/usr/bin/env python3

from hashlib import md5
import sys
import re

PART = 2

SALT = 'qzyelonm'
ORD_A = ord('a')

class Buzzes:
    def __init__(self, init):
        self.data = [init]*16
    def tohex(self, ch):
        if '0'<=ch<='9':
            return int(ch)
        return ord(ch) + 10 - ORD_A
    def __getitem__(self, key):
        return self.data[self.tohex(key)]
    def __setitem__(self, key, value):
        self.data[self.tohex(key)] = value
    def __len__(self):
        return len(self.data)
    def __repr__(self):
        return repr(self.data)

def enumerate_hashes(salt, start=0, stop=None):
    index = start
    while index!=stop:
        h = get_hash(salt, index)
        yield (index, h)
        index += 1

def get_hash(salt, index, cache=[]):
    while len(cache) <= index:
        cache.append(make_hash(salt+str(len(cache))))
    return cache[index]

if PART<2:
    def make_hash(text):
        return md5(text.encode('ascii')).hexdigest()
else:
    def make_hash(text):
        for _ in range(2017):
            text = md5(text.encode('ascii')).hexdigest()
        return text
    
def find_keys(salt, ptn=re.compile(r'(.)\1\1')):
    DURATION = 1000
    buzzes = Buzzes(-2*DURATION)
    for i,h in enumerate_hashes(salt):
        m = ptn.search(h)
        if m:
            k = m.group(1)
            sought = k*5
            if any(sought in v for _,v in enumerate_hashes(salt, i+1, i+1001)):
                yield i


def print_keys(salt):
    i = 0
    for k in find_keys(salt):
        print(k)
        i += 1
        if i>= 64:
            break        

def main(salt):
    print_keys(salt)

if __name__ == '__main__':
    salt = sys.argv[1] if len(sys.argv) > 1 else SALT
    main(salt)
