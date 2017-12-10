#!/usr/bin/env python3

import clip
import sys
import re

class Sub:
    def __init__(self, start, end, reach, repeats):
        self.start = start
        self.end = end
        self.reach = reach
        self.repeats = repeats
        self.mass = None
    def __repr__(self):
        return f'({self.reach}x{self.repeats})'
    def __len__(self):
        return self.end-self.start


class AlterIter:
    def __init__(self, items, start=0, end=None):
        self.items = items
        self._end = end
        self.start = start
        self.index = None
    def __iter__(self):
        return self
    @property
    def next_index(self):
        return self.start if self.index is None else (self.index+1)
    @next_index.setter
    def next_index(self, value):
        self.index = value-1
    @property
    def end(self):
        return self._end if self._end is not None else len(self.items)
    def next(self):
        np = self.next_index
        if np >= self.end:
            raise StopIteration()
        self.index = np
        return self.items[np]
    def replace(self, item):
        self.items[self.index] = item
    def insert(self, item):
        self.items.insert(self.index, item)
    def pop(self):
        return self.data.pop(self.index)
        
    
def find_subs(data):
    pattern = re.compile(r'\(#x#\)'.replace('#', r'([0-9]+)'))
    last = 0
    for m in re.finditer(pattern, data):
        if m.start() > last:
            yield (m.start()-last)
        yield Sub(m.start(), m.end(), int(m.group(1)), int(m.group(2)))
        last = m.end()
    if len(data) > last:
        yield (len(data)-last)


def decompress_length(data):
    subs = list(find_subs(data))
    return subs_length(subs)

def mass(x):
    return x.mass if isinstance(x, Sub) else x

def span(x):
    return len(x) if isinstance(x, Sub) else x

def subs_length(subs):
    i = len(subs)
    while i>0:
        i -= 1
        cur = subs[i]
        if mass(cur) is not None:
            continue
        n = cur.reach
        j = i
        m = 0
        while n > 0:
            j += 1
            nx = subs[j]
            sx = span(nx)
            mx = mass(nx)
            if sx==n:
                m += mx
                n = 0
                break
            if sx < n:
                n -= sx
                m += mx
                continue
            m += n
            n = 0
        cur.mass = (cur.repeats-1) * m
    for x in subs:
        print(x, mass(x))
    return sum(map(mass, subs))
        
                

def main():
    if len(sys.argv) > 1:
        x = ' '.join(sys.argv[1:])
    else:
        print("Press enter to paste.")
        input()
        x = clip.paste()
    x = re.sub(r'\s+','',x)
    ld = decompress_length(x)
    print(f"Length: {ld}")

if __name__ == '__main__':
    main()
