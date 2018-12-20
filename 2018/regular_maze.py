#!/usr/bin/env python3

"""Generates the maze from the regular expression for 2018/20."""

import sys

from enum import Enum
from collections import defaultdict, namedtuple

DIRECTIONS = { 'N': (0,-1), 'E': (1,0), 'S': (0,1), 'W':  (-1,0) }

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

class TokenType(Enum):
    PATH = ''
    LPAREN = '('
    RPAREN = ')'
    OR = '|'
    def __repr__(self):
        return self.name
    @classmethod
    def forchar(cls, value):
        return cls._value2member_map_.get(value, TokenType.PATH)

Token = namedtuple('Token', 'type depth content', defaults=(None,))
    
def lex(expression):
    path_began = None
    depth = 0
    for i,ch in enumerate(expression):
        ttype = TokenType.forchar(ch)
        if path_began is not None:
            if ttype==TokenType.PATH:
                continue
            path = expression[path_began:i]
            path_began = None
            yield Token(type=TokenType.PATH, depth=depth, content=path)
        if ttype==TokenType.PATH:
            path_began = i
        else:
            if ttype==TokenType.RPAREN:
                depth -= 1
            yield Token(type=ttype, depth=depth)
            if ttype==TokenType.LPAREN:
                depth += 1
    if path_began is not None:
        path = expression[path_began:]
        yield Token(type=TokenType.PATH, depth=depth, content=path)

def validate(tokens):
    # Check that every parenthesis is surrounding some alternatives
    for i,tok in enumerate(tokens):
        if tok.type==TokenType.LPAREN:
            j = tokens.index(Token(TokenType.RPAREN, tok.depth), i+1)
            k = tokens.index(Token(TokenType.OR, tok.depth+1), i+1)
            assert i < k < j
    assert tokens.index(Token(TokenType.RPAREN, 0))==len(tokens)-1

def token_split_ors(tokens):
    depth = tokens[0].depth
    current = []
    sought = Token(TokenType.OR, depth)
    for x in tokens:
        if x==sought:
            yield current
            current = []
        else:
            current.append(x)
    yield current

def token_split_chain(tokens):
    current = None
    for x in tokens:
        if current is None:
            if x.type==TokenType.LPAREN:
                current = [x]
            else:
                yield [x]
        else:
            current.append(x)
            if x.type==TokenType.RPAREN and x.depth==current[0].depth:
                yield current
                current = None
    assert current is None
    
def follow(starts, tokens, doors):
    while tokens and tokens[0].type==TokenType.LPAREN:
        r = tokens.index(Token(TokenType.RPAREN, tokens[0].depth))
        if r!=len(tokens)-1:
            break
        tokens = tokens[1:-1]
    if not tokens:
        return starts
    tok = tokens[0]
    if len(tokens)==1:
        if tok.type==TokenType.OR:
            return starts
        assert tok.type==TokenType.PATH
        path = tok.content
        return { run_path(pos, path, doors) for pos in starts }
    if Token(TokenType.OR, tok.depth) in tokens:
        alts = list(token_split_ors(tokens))
        return set.union(*(follow(starts, alt, doors) for alt in alts))
    chain = list(token_split_chain(tokens))
    positions = starts
    for sub in chain:
        positions = follow(positions, sub, doors)
    return positions

def run_path(start, path, doors, dirs=DIRECTIONS):
    cur = start
    for ch in path:
        new = addp(cur, dirs[ch])
        doors[cur].add(new)
        doors[new].add(cur)
        cur = new
    return cur

class DisplayMaze:
    def __init__(self, doors, positions, start=(0,0)):
        self.x0 = min(x for x,y in doors)
        self.y0 = min(y for x,y in doors)
        self.x1 = max(x for x,y in doors) + 1
        self.y1 = max(y for x,y in doors) + 1
        self.width = (self.x1-self.x0)*2+1
        self.height = (self.y1-self.y0)*2+1
        self.doors = doors
        self.positions = positions
        self.start = start
    def __getitem__(self, pos):
        x,y = pos
        if x%2==0 and y%2==0:
            return '#'
        rx = self.x0 + x//2
        ry = self.y0 + y//2
        if x%2==0:
            return '|' if (rx-1,ry) in self.doors[rx,ry] else '#'
        if y%2==0:
            return '-' if (rx,ry-1) in self.doors[rx,ry] else '#'
        if (rx,ry) in self.positions:
            return '*' if (rx,ry)==self.start else 'D'
        return 'X' if (rx,ry)==self.start else ' '

def display(doors, positions):
    maze = DisplayMaze(doors, positions)
    xran = range(maze.width)
    for y in range(maze.height):
        print(''.join(maze[x,y] for x in xran))
        

def main():
    expression = sys.stdin.read().strip().lstrip('^').rstrip('$')
    tokens = list(lex(expression))
    validate(tokens)
    doors = defaultdict(set)
    positions = follow({(0,0)}, tokens, doors)
    display(doors, positions)

if __name__ == '__main__':
    main()
