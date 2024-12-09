#!/usr/bin/env python3

import sys

def read_data():
    pos = 0
    counter = 0
    spaces = []
    isfile = True
    data = []
    for size in map(int, sys.stdin.read().strip()):
        if isfile:
            data += [counter]*size
            counter += 1
        else:
            data += [None]*size
            spaces.extend(range(pos, pos+size))
        pos += size
        isfile = not isfile
    return data, spaces

def frag_data(data, spaces):
    end = len(data)-1
    for target in spaces:
        while target < end and data[end] is None:
            end -= 1
        if target >= end:
            break
        data[target] = data[end]
        data[end] = None
        end -= 1

def file_start_size(data, index):
    while index >= 0 and data[index] is None:
        index -= 1
    if index < 0:
        return (-1,-1)
    id = data[index]
    start = index
    while start > 0 and data[start-1]==id:
        start -= 1
    return (start, index+1-start)

def find_space(data, source, size):
    run = 0
    for i,sp in enumerate(data):
        if i >= source:
            break
        if sp is not None:
            run = 0
        else:
            run += 1
            if run >= size:
                return i + 1 - run
    return -1

def move_data(data, src, dest, size):
    for i in range(size):
        data[dest+i] = data[src+i]
        data[src+i] = None

def frag_files(data):
    start, size = file_start_size(data, len(data)-1)
    while start >= 0:
        sp = find_space(data, start, size)
        if sp >= 0:
            move_data(data, start, sp, size)
        start, size = file_start_size(data, start-1)

def checksum_data(data):
    return sum(i*d for i,d in enumerate(data) if d)

def main():
    data, spaces = read_data()
    original_data = data[:]
    frag_data(data, spaces)
    print(checksum_data(data))
    data = original_data
    frag_files(data)
    print(checksum_data(data))

if __name__ == '__main__':
    main()
