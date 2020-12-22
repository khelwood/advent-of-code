#!/usr/bin/env python3

import sys

class Player:
    def __init__(self, name, cards=None):
        self.name = name
        self.cards = cards or []
    def __len__(self):
        return len(self.cards)
    def push(self, card):
        self.cards.append(card)
    def pop(self):
        return self.cards.pop(0)
    def calculate_score(self):
        return sum(i*card for (i,card) in enumerate(reversed(self.cards), 1))
    def __iadd__(self, other):
        self.cards.extend(other)
    def __repr__(self):
        return self.name
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.cards[index]
        cards = self.cards[index]
        return Player(self.name, cards)


def combat(player1, player2):
    a = player1.pop()
    b = player2.pop()
    if a > b:
        player1 += (a,b)
    else:
        player2 += (b,a)

def recombat(player1, player2):
    history = set()
    while player1 and player2:
        current = (tuple(player1.cards), tuple(player2.cards))
        if current in history:
            return player1
        history.add(current)
        a = player1.pop()
        b = player2.pop()
        if len(player1) < a or len(player2) < b:
            winner = player1 if a > b else player2
        else:
            winner = recombat(player1[:a], player2[:b])
            if winner.name==player1.name:
                winner = player1
            else:
                winner = player2
        winner += ((a,b) if winner==player1 else (b,a))
    return player1 or player2


def read_cards():
    players = []
    for i in range(1,3):
        name = next(sys.stdin).strip().rstrip(':')
        assert name==f'Player {i}'
        pl = Player(name)
        for line in sys.stdin:
            line = line.strip()
            if not line:
                break
            pl.push(int(line))
        players.append(pl)
    return players


def main():
    player1, player2 = read_cards()
    original1 = player1[:]
    original2 = player2[:]
    rounds = 0
    while player1 and player2:
        rounds += 1
        combat(player1, player2)
    winner = player1 or player2
    print("Normal combat:")
    print(winner, "score:", winner.calculate_score())
    print("Recursive combat:")
    winner = recombat(original1, original2)
    print(winner, "score:", winner.calculate_score())


if __name__ == '__main__':
    main()
