#!/usr/bin/env python3

import sys
import json

def number_total(json_data, ignore_red):
    n = 0
    if isinstance(json_data, int):
        return json_data
    elif isinstance(json_data, dict):
        for k,v in json_data.items():
            if ignore_red and (k=="red" or v=="red"):
                return 0
            n += number_total(k, ignore_red)
            n += number_total(v, ignore_red)
    elif isinstance(json_data, list):
        for v in json_data:
            n += number_total(v, ignore_red)
    return n

def main():
    json_text = sys.stdin.read().strip()
    json_data = json.loads(json_text)
    total = number_total(json_data, False)
    print("int total:", total)
    total = number_total(json_data, True)
    print("int total avoiding red:", total)

if __name__ == '__main__':
    main()
