#!/usr/bin/env python3

import pyperclip

PART = 2

ORDA = ord('a')

def extract_letter(letters):
    counts = [0]*26
    for ch in letters:
        counts[ord(ch)-ORDA] += 1
    if PART==2:
        m = min(filter(bool, counts))
    else:
        m = max(counts)
    i = counts.index(m)
    return chr(ORDA+i)

def columns(lines):
    return zip(*lines)

def main():
    print("Copy message to clipboard and press enter.")
    input()
    block = pyperclip.paste().strip()
    lines = block.split('\n')
    message = ''.join(map(extract_letter, columns(lines)))
    print(f"Message: {message}")

if __name__ == '__main__':
    main()
