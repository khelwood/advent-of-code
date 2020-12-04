#!/usr/bin/env python3

import sys
import re

REQUIRED_FIELDS = {
    'byr': r'(19[2-9][0-9])|(200[0-2])',
    'iyr': r'20(1[0-9]|20)',
    'eyr': r'20(2[0-9]|30)',
    'hgt': r'(1([5-8][0-9]|9[0-3]))cm|(59|6[0-9]|7[0-6])in',
    'hcl': r'#[0-9a-f]{6}',
    'ecl': r'amb|blu|brn|gry|grn|hzl|oth',
    'pid': r'[0-9]{9}',
}

REQUIRED_FIELDS = {k:re.compile(f'^({v})$')
                       for (k,v) in REQUIRED_FIELDS.items()}

def parse_passport(text):
    d = {}
    for m in re.finditer(r'\b(\w+):(\S+)\b', text):
        d[m.group(1)] = m.group(2)
    return d

def group_passports(text):
    return text.split('\n\n')

def passport_has_fields(dct, required=REQUIRED_FIELDS):
    return all(f in dct for f in required)

def passport_has_valid_values(dct, required=REQUIRED_FIELDS):
    for s,regex in required.items():
        value = dct.get(s)
        if value is None or not regex.match(value):
            return False
    return True

def main():
    passports = [parse_passport(block)
                     for block in group_passports(sys.stdin.read().strip())]
    print("Num with valid fields:",
              sum(map(passport_has_fields, passports)))
    print("Num with valid values:",
              sum(map(passport_has_valid_values, passports)))

if __name__ == '__main__':
    main()
