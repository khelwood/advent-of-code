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

def checksum_data(data):
    return sum(i*d for i,d in enumerate(data) if d)

# Part 2

class File:
    def __init__(self, id, size):
        self.id = id
        self.size = size
    def checksum(self, start):
        if not self.id:
            return 0
        end = start + self.size-1
        sumrange = self.size*(start+end)//2
        return self.id * sumrange

def read_files(text):
    files = []
    counter = 0
    isfile = True
    for size in map(int, text):
        if isfile:
            f = File(counter, size)
            counter += 1
        else:
            f = File(None, size)
        files.append(f)
        isfile = not isfile
    return files

def frag_files(files):
    for si in range(len(files)-1, 0, -1):
        src = files[si]
        if src.id is None:
            continue
        for ti in range(1, si):
            tgt = files[ti]
            if tgt.id is not None or tgt.size < src.size:
                continue
            tgt.size -= src.size
            files[si] = File(None, src.size)
            files.insert(ti, src)
            break

def checksum_files(files):
    pos = 0
    total = 0
    for f in files:
        total += f.checksum(pos)
        pos += f.size
    return total

def main():
    text = sys.stdin.read().strip()
    data, spaces = read_data(text)
    frag_data(data, spaces)
    print(checksum_data(data))
    files = read_files(text)
    frag_files(files)
    print(checksum_files(files))

if __name__ == '__main__':
    main()
