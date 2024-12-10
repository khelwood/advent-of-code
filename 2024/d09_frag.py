#!/usr/bin/env python3

import sys

# Part 1

def read_data(text):
    pos = 0
    counter = 0
    spaces = []
    isfile = True
    data = []
    for size in map(int, text):
        if isfile:
            data += [counter]*size
            counter += 1
        elif size > 0:
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

def checksum_data(data):
    return sum(i*d for i,d in enumerate(data) if d)

# Part 2

class File:
    def __init__(self, id, start, size):
        self.id = id
        self.start = start
        self.size = size
    @property
    def last(self):
        return self.start + self.size - 1
    def checksum(self):
        if not self.id:
            return 0
        sumrange = self.size * (self.start + self.last)//2
        return self.id * sumrange

def read_files(text):
    files = []
    spaces = []
    pos = 0
    counter = 0
    isfile = True
    for size in map(int, text):
        if isfile:
            files.append(File(counter, pos, size))
            counter += 1
        elif size > 0:
            spaces.append(File(None, pos, size))
        isfile = not isfile
        pos += size
    return files, spaces

def find_space(src, spaces):
    for space in spaces:
        if space.start >= src.start:
            break
        if space.size >= src.size:
            return space
    return None

def frag_files(files, spaces):
    for src in reversed(files):
        space = find_space(src, spaces)
        if space is not None:
            src.start = space.start
            space.start += src.size
            space.size -= src.size
            if space.size==0:
                spaces.remove(space)

def checksum_files(files):
    return sum(f.checksum() for f in files)

def main():
    text = sys.stdin.read().strip()
    data, spaces = read_data(text)
    frag_data(data, spaces)
    print(checksum_data(data))
    files, spaces = read_files(text)
    frag_files(files, spaces)
    print(checksum_files(files))

if __name__ == '__main__':
    main()
