#!/usr/bin/env python3

import clip

def remove_junk(text):
    output = []
    j = 0
    i = text.find('<')
    while i >= 0:
        if i>j:
            output.append(text[j:i])
        j = find_junk_end(text, i)+1
        i = text.find('<', j)
    if j < len(text):
        output.append(text[j:])
    return ''.join(output)

def count_garbage(text):
    count = 0
    j = 0
    i = text.find('<')
    while i>=0:
        j = find_junk_end(text, i)
        count += count_junk_innards(text, i+1, j)
        j += 1
        i = text.find('<', j)
    return count

def count_junk_innards(text, start, end):
    count = 0
    i = start
    while i < end:
        if text[i]=='!':
            i += 2
        else:
            count += 1
            i += 1
    return count

def find_junk_end(text, start):
    i = start
    while True:
        ch = text[i]
        if ch=='>':
            return i
        i += 1 + (ch=='!')

def score_text(text):
    score = 0
    depth = 0
    for ch in text:
        if ch=='{':
            depth += 1
        if ch=='}':
            assert depth > 0
            score += depth
            depth -= 1
    assert depth==0
    return score

def process(text):
    text = remove_junk(text)
    score = score_text(text)
    return score

def main():
    print("Press enter to start.")
    input()
    block = clip.paste().strip()
    print("Score:", process(block))
    print("Garbage count:", count_garbage(block))

if __name__ == '__main__':
    main()
