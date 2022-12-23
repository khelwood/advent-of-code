#!/usr/bin/env python3

import sys

DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))

def addp(a,b):
    return (a[0]+b[0], a[1]+b[1])

def read_maze():
    maze = {}
    for y,line in enumerate(sys.stdin):
        for x,ch in enumerate(line.strip()):
            if ch=='S':
                start = (x,y)
                v = 0
            elif ch=='E':
                end = (x,y)
                v = 27
            else:
                v = 1 + ord(ch) - ord('a')
            maze[x,y] = v
    return maze,x+1,y+1,start,end

def score_maze(maze, end, dirs=DIRECTIONS):
    scores = {}
    scores[end] = 0
    curgen = [end]
    while curgen:
        nextgen = []
        for p in curgen:
            v = maze[p]
            for dir in dirs:
                n = addp(p, dir)
                vn = maze.get(n, -10)
                if vn >= v-1 and n not in scores:
                    nextgen.append(n)
                    scores[n] = scores[p] + 1
        curgen = nextgen
    return scores

def main():
    maze,w,h,start,end = read_maze()
    scores = score_maze(maze, end)
    print("Steps from initial start:", scores[start])
    new_start = min((p for p in scores if maze[p]==1), key=lambda p:scores[p])
    print("Steps from new start:", scores[new_start])

if __name__ == '__main__':
    main()
