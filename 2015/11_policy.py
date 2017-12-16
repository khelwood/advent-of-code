#!/usr/bin/env python3

import sys

def numbers_valid(numbers):
    return (contains_sequence_of_three(numbers)
            and no_ambiguous_letters(numbers)
            and contains_two_pairs(numbers))

def contains_sequence_of_three(numbers):
    return any(numbers[i]+2==numbers[i+1]+1==numbers[i+2]
                for i in range(len(numbers)-2))

def no_ambiguous_letters(numbers):
    bad = {ord(ch) for ch in 'ilo'}
    return not any(n in bad for n in numbers)

def contains_two_pairs(numbers):
    num_pairs = 0
    i = 0
    while i < len(numbers)-1:
        if numbers[i]==numbers[i+1]:
            if num_pairs:
                return True
            num_pairs += 1
            i += 2
        else:
            i += 1
    return False

def increment(numbers):
    i = len(numbers)-1
    while numbers[i]==25:
        numbers[i] = 0
        i -= 1
    numbers[i] += 1

def increment_valid(numbers):
    increment(numbers)
    while not numbers_valid(numbers):
        increment(numbers)

def main(text):
    numbers = [ord(ch)-ord('a') for ch in text.strip()]
    print(' ...', end='\r')
    increment_valid(numbers)
    result = ''.join([chr(n+ord('a')) for n in numbers])
    print(result)
    print(' ...', end='\r')
    increment_valid(numbers)
    result = ''.join([chr(n+ord('a')) for n in numbers])
    print(result)    

if __name__ == '__main__':
    if len(sys.argv)!=2:
        exit("Usage: %s <text>"%sys.argv[0])
    main(sys.argv[1])
