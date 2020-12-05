#!/usr/bin/env python3

import sys

def seat_code_to_pos(line):
    row0 = 0
    row1 = 128
    col0 = 0
    col1 = 8
    for ch in line:
        if ch=='F':
            row1 = (row0 + row1)//2
        elif ch=='B':
            row0 = (row0 + row1)//2
        elif ch=='L':
            col1 = (col0 + col1)//2
        elif ch=='R':
            col0 = (col0 + col1)//2
        else:
            raise ValueError("Invalid seat code: %r"%line)
    assert row1==row0+1
    assert col1==col0+1
    return (row0, col0)

def seat_pos_to_id(row, col):
    return row*8 + col

def main():
    if len(sys.argv) > 1:
        for code in sys.argv[1:]:
            r,c = seat_code_to_pos(code)
            id = seat_pos_to_id(r,c)
            print(f"{code}: row {r}, column {c}, seat ID {id}.")
        return
    positions = list(map(seat_code_to_pos, sys.stdin.read().split()))
    seat_ids = [seat_pos_to_id(r,c) for (r,c) in positions]
    print("Highest seat id:", max(seat_ids))

    seat_ids.sort()
    last = seat_ids[0]-1
    for seat_id in seat_ids:
        if seat_id == last + 2:
            print("Missing seat id:", last+1)
            break
        last = seat_id

if __name__ == '__main__':
    main()
