#!/usr/bin/env python3

import sys

BLACK = '0'
WHITE = '1'
TRANSPARENT = '2'

def split_layers(data, layer_size):
    return [data[i:i+layer_size:] for i in range(0, len(data), layer_size)]

def fewest_zeroes_layer(layers):
    best_nz = len(layers[0])
    best = None
    for layer in layers:
        nz = layer.count('0')
        if nz < best_nz:
            best_nz = nz
            best = layer
    return best

def get_colour_at_index(layers, index):
    for layer in layers:
        li = layer[index]
        if li != TRANSPARENT:
            return li
    return TRANSPARENT

def draw(layers, width, height):
    index = 0
    for y in range(height):
        for x in range(width):
            co = get_colour_at_index(layers, index)
            index += 1
            print('\u2588' if co==WHITE else ' ', end='')
        print()

def main():
    data = sys.stdin.read().strip()
    width = 25
    height = 6
    layers = split_layers(data, width*height)
    layer = fewest_zeroes_layer(layers)
    ones = layer.count('1')
    twos = layer.count('2')
    print("Part one:", ones*twos)
    print("\nPart two:")
    draw(layers, width, height)

if __name__ == '__main__':
    main()
