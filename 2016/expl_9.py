#!/usr/bin/env python3

import clip
import sys

def iter_decompress(data):
    j=0
    i = data.find('(')
    while i>=0:
        if i>j:
            yield data[j:i]
        i += 1
        j = data.index(')',i)
        x = data.index('x',i)
        n = int(data[i:x])
        r = int(data[x+1:j])
        j += 1
        txt = data[j:j+n]
        for _ in range(r):
            yield txt
        j += n
        i = data.find('(',j)
    if j < len(data):
        yield data[j:]

def decompress(data):
    return ''.join(iter_decompress(data))

def main():
    if len(sys.argv) > 1:
        x = ' '.join(sys.argv[1:]).strip()
    else:
        print("Press enter to paste.")
        input()
        x = clip.paste().strip()
    d = decompress(x)
    if len(d) < 80:
        print(d)
    print(f"\nLength: {len(d)}")

if __name__ == '__main__':
    main()
