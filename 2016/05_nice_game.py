#!/usr/bin/env python3

from hashlib import md5

def find_hashes(door):
    i = 0
    ni = 100000
    while True:
        i += 1
        if i>=ni:
            print(f'    {i}   ', end='\r')
            ni += 100000
        h = make_hash(door, i)
        if hash_ok(h):
            yield h

def make_password(door, length=8):
    results = ['.']*length
    found = 0
    for h in find_hashes(door):
        hd = h.hexdigest()
        i = ord(hd[5])-ord('0')
        if 0<=i<length and results[i]=='.':
            results[i] = hd[6]
            print('   %r   '%(''.join(results)))
            found += 1
            if found >= length:
                break
    return ''.join(results)

def make_hash(door, i):
    s = door+str(i)
    return md5(s.encode('ascii'))

def hash_ok(h):
    return h and h.hexdigest().startswith('00000')

def main():
    door = input('Enter door id: ').strip()
    print(f'Door id: {door}')
    password = make_password(door)
    print(f'\nPassword: {password}')

if __name__ == '__main__':
    main()
