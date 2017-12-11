#!/usr/bin/env python3

import pyperclip

def abba(txt):
    for i in range(len(txt)-3):
        a = txt[i]
        b = txt[i+1]
        if a!=b and b==txt[i+2] and a==txt[i+3]:
            return True
    return False

def find_abas(txts):
    for txt in txts:
        for i in range(len(txt)-2):
            a = txt[i]
            if a == txt[i+2] != txt[i+1]:
                yield txt[i:i+3]

def separate(txt):
    j = 0
    good = []
    bad = []
    i = txt.find('[')
    while i>=0:
        if i>j:
            good.append(txt[j:i])
        j = txt.index(']', i+1)
        bad.append(txt[i+1:j])
        j += 1
        i = txt.find('[',j)
    if j < len(txt):
        good.append(txt[j:])
    return good, bad

def supports_ssl(txt):
    good, bad = separate(txt)
    abas = set(find_abas(good))
    babs = [b+a+b for a,b,_ in abas]
    return any(bab in b for b in bad for bab in babs)

def supports_abba(txt):
    good, bad = separate(txt)
    return any(map(abba, good)) and not any(map(abba, bad))

def count(fn, lines):
    return sum(map(fn, lines))

def main():
    print("Press enter to start")
    input()
    block = pyperclip.paste().strip()
    lines = block.split('\n')
    c = count(supports_abba, lines)
    print("ABBA count:", c)
    d = count(supports_ssl, lines)
    print("SSL count:", d)
        

if __name__ == '__main__':
    main()
