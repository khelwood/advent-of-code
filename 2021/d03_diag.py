#!/usr/bin/env python3

import sys

def find_gamma_string(lines):
    ln = len(lines[0])
    counts = [0]*ln
    for line in lines:
        for i,ch in enumerate(line):
            if ch=='1':
                counts[i] += 1
    h = len(lines)//2
    return ''.join('1' if c >= h else '0' for c in counts)

def find_gas_level(lines, co2:bool):
    """
    * Find X = most common first bit (1 if there's a tie)
    * If co2 then switch the value of X
    * Eliminate all values whose first bit is not X
    * Find X for second bit
    * Eliminate all values whose secont bit is not X
    * Proceed until one value is left
    """
    pos = 0
    while len(lines) > 1:
        ones = sum(line[pos]=='1' for line in lines)
        sel = '1' if 2*ones >= len(lines) else '0'
        if co2:
            sel = '0' if sel=='1' else '1'
        lines = [line for line in lines if line[pos]==sel]
        pos += 1
    return lines[0]

def main():
    lines = sys.stdin.read().strip().splitlines()
    gamma_string = find_gamma_string(lines)
    epsilon_string = ''.join('0' if ch=='1' else '1' for ch in gamma_string)
    gamma = int(gamma_string, 2)
    epsilon = int(epsilon_string, 2)
    print(f"Gamma: {gamma}, Epsilon: {epsilon}")
    print("Product:", gamma*epsilon)
    o2_string = find_gas_level(lines, False)
    co2_string = find_gas_level(lines, True)
    o2 = int(o2_string, 2)
    co2 = int(co2_string, 2)
    print(f"O2: {o2}, CO2: {co2}")
    print("Product:", o2*co2)

if __name__ == '__main__':
    main()
