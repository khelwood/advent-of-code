#!/usr/bin/env python3

import sys
import itertools

WID = HEI = 5

def board_positions(XR=range(WID), YR=range(HEI)):
    return itertools.product(XR, YR)

class Board:
    def __init__(self):
        self.numbers = {}
        self.marked = set()
        self.last_num = None
    def __getitem__(self, pos):
        return self.numbers[pos]
    def __setitem__(self, pos, value):
        self.numbers[pos] = value
    def row_wins(self, y):
        return all((x,y) in self.marked for x in range(WID))
    def col_wins(self, x):
        return all((x,y) in self.marked for y in range(HEI))
    def mark(self, value):
        for p in board_positions():
            if self[p]==value:
                self.marked.add(p)
                if self.row_wins(p[1]) or self.col_wins(p[0]):
                    self.last_num = value
                    return True
        return False
    def final_score(self):
        return (self.last_num *
              sum(self[p] for p in board_positions() if p not in self.marked))

def read_bingo():
    line_iter = iter(sys.stdin.read().strip().splitlines())
    calls = [int(n) for n in next(line_iter).replace(',',' ').split()]
    boards = list(read_boards(line_iter))
    return boards, calls

def read_boards(line_iter):
    while True:
        boardlines = []
        for line in line_iter:
            line = line.strip()
            if not line:
                if boardlines:
                    break
                continue
            boardlines.append(line)
        if not boardlines:
            break
        board = Board()
        for y,line in enumerate(boardlines):
            for x,n in enumerate(line.split()):
                board[x,y] = int(n)
        yield board

def play_all_boards(boards, calls):
    won_boards = []
    for num in calls:
        anywon = False
        for board in boards:
            if board.mark(num):
                won_boards.append(board)
                anywon = True
        if anywon:
            boards = [board for board in boards if board.last_num is None]
        if not boards:
            break
    return won_boards

def main():
    boards, calls = read_bingo()
    won_boards = play_all_boards(boards, calls)
    print("Final score to win:", won_boards[0].final_score())
    print("Final score to lose:", won_boards[-1].final_score())

if __name__ == '__main__':
    main()
