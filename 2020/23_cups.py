#!/usr/bin/env python3

import sys

class Cups:
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return ' '.join(
            f'({v})' if i==0 else str(v) for (i,v) in enumerate(self.values)
        )

    def move(self):
        values = self.values
        label = values[0]
        pickup = values[1:4]
        del values[1:4]
        destindex = -1
        destlabel = -1
        maxlabel = -1
        maxindex = -1
        for i,c in enumerate(values):
            if destlabel < c < label:
                destindex = i
                destlabel = c
            if maxlabel < c:
                maxindex = i
                maxlabel = c
        if destindex < 0:
            destindex = maxindex
        destindex += 1
        values[destindex:destindex] = pickup
        prev = values.index(label)
        current = (prev+1)%len(values)
        self.values = values[current:] + values[:current]

    def __len__(self):
        return len(self.values)

    @property
    def output(self):
        i = self.values.index(1)
        return ''.join(map(str, self.values[i+1:] + self.values[:i]))
            

def main():
    arg = sys.argv[1] if len(sys.argv)>1 else input()
    initial = tuple(map(int, arg))
    cups = Cups(list(initial))
    for _ in range(100):
        cups.move()
    print(cups.output)


if __name__ == '__main__':
    main()
