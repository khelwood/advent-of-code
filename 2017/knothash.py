import functools
import operator

class Loop:
    DEFAULT_LENGTH = 256
    def __init__(self, length=None):
        if length is None:
            length = self.DEFAULT_LENGTH
        self.data = list(range(length))
        self.cur = 0
        self.skip = 0
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data[index] = value
    def __str__(self):
        return '('+' '.join(['[%r]'%x if i==self.cur else repr(x)
                                 for i,x in enumerate(self.data)]) + ')'
    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
    def twist(self, length):
        L = len(self)
        for i in range(length//2):
            self.swap((self.cur+i)%L, (self.cur + length - i - 1) % L)
        self.cur = (self.cur + length + self.skip)%L
        self.skip = (self.skip + 1)%L
    def apply_twists(self, lengths, repeats=1):
        for _ in range(repeats):
            for length in lengths:
                self.twist(length)
    def knothash(self):
        dense = [functools.reduce(operator.xor, self.data[i:i+16])
                     for i in range(0, len(self), 16)]
        return ''.join([format(n, '02x') for n in dense])

