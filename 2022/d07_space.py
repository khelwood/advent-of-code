#!/usr/bin/env python3

import sys

class File:
    def __init__(self, name, parent, size=0, dir=False):
        self.name = name
        self.parent = parent
        self._size = size
        self.dir = dir
        self.contents = []
    @property
    def size(self):
        if self.dir:
            return sum(f.size for f in self.contents)
        return self._size
    @property
    def root(self):
        return self.parent.root if self.parent else self
    def select(self, path):
        if not path or path=='.':
            return self
        if path=='..':
            return self.parent
        if path.startswith('/'):
            return self.root.select(path[1:])
        first, _, rest = path.rstrip('/').partition('/')
        child = next(f for f in self.contents if f.name==first)
        return child if not rest else child.select(rest)
    def add_child(self, desc):
        size, _, name = desc.partition(' ')
        if size=='dir':
            f = File(name, self, dir=True)
        else:
            f = File(name, self, size=int(size))
        self.contents.append(f)
        return f
    def print_tree(self, indent=''):
        if self.dir:
            print(f'{indent}- {self.name} (dir)')
            for c in self.contents:
                c.print_tree(indent+'  ')
        else:
            print(f'{indent}- {self.name} (file, size={self.size})')
    def walk(self):
        yield self
        if self.dir:
            for c in self.contents:
                yield from c.walk()


def create_fs(commands):
    root = File('/','',dir=True)
    wd = root
    i = 0
    while i < len(commands):
        i, wd = run_command(commands, i, wd, root)
    return root

def run_command(commands, i, wd, root):
    cmd = commands[i]
    i += 1
    if not cmd.startswith('$ '):
        raise ValueError(cmd)
    if cmd.startswith('$ cd '):
        name = cmd[5:].strip()
        return i, wd.select(name)
    if cmd.startswith('$ ls'):
        while i < len(commands) and not commands[i].startswith('$'):
            wd.add_child(commands[i])
            i += 1
        return i, wd


def main():
    commands = sys.stdin.read().strip().splitlines()
    root = create_fs(commands)
    root.print_tree()
    dir_sizes = [d.size for d in root.walk() if d.dir]
    print("Total:", sum(size for size in dir_sizes if size <= 100000))
    deficit = root.size - 40000000
    best_size = min(size for size in dir_sizes if size >= deficit)
    print("Best size:", best_size)

if __name__ == '__main__':
    main()
