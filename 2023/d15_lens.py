#!/usr/bin/env python3

import sys

from collections import namedtuple

Lens = namedtuple('Lens', 'label fl')

def string_hash(string, *, cache={}):
    h = cache.get(string)
    if h is not None:
        return h
    h = 0
    for ch in string:
        h += ord(ch)
        h *= 17
        h %= 256
    cache[string] = h
    return h

def find_lens(box, label):
    return next((i for (i,x) in enumerate(box) if x.label==label), -1)

def process_lens(boxes, string):
    if string[-1]=='-':
        label = string[:-1]
        op = '-'
    else:
        label = string[:-2]
        op = '='
        fl = int(string[-1])
    h = string_hash(label)
    box = boxes[h]
    i = find_lens(box, label)
    if i >= 0:
        if op=='-':
            del box[i]
        else:
            box[i] = Lens(label, fl)
    elif op=='=':
        box.append(Lens(label, fl))

def power(boxes):
    total = 0
    for bi, box in enumerate(boxes, 1):
        total += bi*sum(lens.fl*i for (i,lens) in enumerate(box, 1))
    return total

def main():
    strings = sys.stdin.read().strip().split(',')
    total = sum(map(string_hash, strings))
    print("Total hash:", total)
    boxes = [[] for _ in range(256)]
    for string in strings:
        process_lens(boxes, string)
    print("Power:", power(boxes))

if __name__ == '__main__':
    main()
