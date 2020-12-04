#!/usr/bin/env python3

import sys
import re
from itertools import chain, combinations

from intcode import Program, parse_program_input

ROOMS = {}

class Room:
    def __init__(self, name, exits):
        self.name = name
        self.exits = {x:None for x in exits}
    def explored(self):
        return all(self.exits.values())
    def __repr__(self):
        return 'Room(%r)'%self.name
    def show(self):
        print(f"[{self.name}]")
        print(f"[Exits: {self.exits}]")
    def direction_to(self, room):
        return next((k for (k,v) in self.exits.items() if v==room), None)

def powerset(items):
    items = list(items)
    return chain.from_iterable(combinations(items, r)
                                for r in range(len(items)+1))

def find_explore(room, directions='north south east west'.split()):
    reached = {room}
    new = [((), room)]
    while new:
        old = new
        new = []
        while old:
            route, room = old.pop()
            for direc in directions:
                dest = room.exits.get(direc, 'nothing')
                if dest is None:
                    return route + (direc,)
                if isinstance(dest, Room) and dest not in reached:
                    reached.add(dest)
                    new.append((route + (direc,), dest))
    return None

def find_path(start, end, directions='north south east west'.split()):
    if start==end:
        return []
    reached = {start}
    new = [((), start)]
    while new:
        old = new
        new = []
        while old:
            route, room = old.pop()
            for direc in directions:
                dest = room.exits.get(direc)
                if dest==end:
                    return route + (direc,)
                if isinstance(dest, Room) and dest not in reached:
                    reached.add(dest)
                    new.append((route + (direc,), dest))
    return None

def identify_room(text):
    m = re.search('(?s:.*)== ([^=]+) ==', text)
    if not m:
        return None
    return m.group(1)

def identify_exits(text):
    i = text.find('Doors here lead:')
    if i < 0:
        return []
    return items_from(text, text.index('\n', i)+1)

def identify_inventory(text):
    i = text.find('Items in your inventory:')
    if i < 0:
        return []
    return items_from(text, text.index('\n', i)+1)

def identify_items(text):
    i = text.find('Items here:')
    if i < 0:
        return []
    return items_from(text, text.index('\n', i)+1)

def items_from(text, i):
    items = []
    while text.startswith('- ', i):
        j = text.index('\n',i)
        name = text[i+2:j].strip()
        items.append(name)
        i = j+1
    return items

def should_take(item):
    item = item.lower()
    if 'infinite loop' in item:
        return False
    if 'giant electromagnet' in item:
        return False
    if 'molten lava' in item:
        return False
    if 'escape pod' in item:
        return False
    if 'photons' in item:
        return False
    return True
        
class Player:
    def __init__(self, game):
        self.game = game
        self.inventory = []
        self.rooms = {}
        self.game_map = {}
        self.current_room = None
        self.going = None
        self.silent = False

    def play(self):
        self.silent = True
        output = self.issue('')
        self.parse_output(output)
        while self.explore():
            pass
        self.issue('inv')
        checkpoint = ROOMS['Security Checkpoint']
        self.go_to(checkpoint)
        direc = checkpoint.direction_to('blocked')
        self.solve_checkpoint(direc)

    def solve_checkpoint(self, direc):
        self.check_inventory()
        items = self.inventory[:]
        self.silent = True
        for selection in powerset(items):
            print(f"[Trying {selection}]")
            self.make_inventory(selection)
            output = self.issue(direc)
            if "you are ejected back to the checkpoint" not in output:
                print(selection)
                break
        print(output)

    def go_to(self, dest):
        if self.current_room==dest:
            return
        path = find_path(self.current_room, dest)
        for d in path:
            output = self.issue(d)
        self.going = None
        self.parse_output(output)

    def make_inventory(self, selection):
        selection = set(selection)
        setinv = set(self.inventory)
        for sel in (selection-setinv):
            self.take(sel)
        for sel in (setinv-selection):
            self.drop(sel)
        self.check_inventory(selection)
        

    def check_inventory(self, inv=None):
        if inv is None:
            inv = self.inventory
        output = self.issue('inv')
        items = identify_inventory(output)
        extra = set(items)-set(inv)
        missing = set(inv)-set(items)
        if extra or missing:
            raise ValueError(f'Extra: {extra}; missing {missing}')

    def explore(self):
        path = find_explore(self.current_room)
        if not path:
            return False
        print("PATH:", path)
        for d in path:
            output = self.go(d)
        self.parse_output(output)
        return True

    def go(self, direc):
        self.going = direc
        return self.issue(direc)

    def parse_output(self, output):
        r = identify_room(output)
        if r:
            cr = self.current_room
            self.new_room(r, output)
            if self.going and self.current_room!=cr:
                cr.exits[self.going] = self.current_room
                self.going = None
        if self.going:
            self.current_room.exits[self.going] = 'blocked'
            self.going = None
                

    def new_room(self, r, output):
        if self.current_room and r==self.current_room.name:
            return
        room = ROOMS.get(r)
        if room is None:
            exits = identify_exits(output)
            room = Room(r, exits)
            items = identify_items(output)
            for item in items:
                if should_take(item):
                    self.take(item)
            ROOMS[r] = room
        self.current_room = room
        room.show()

    def issue(self, command):
        if not self.silent:
            print(">>", command.upper())
        if command:
            command = command.strip() + '\n'
        self.game.run_input(command)
        return self.flush()

    def flush(self):
        output = ''.join(map(chr, self.game.output_values))
        self.game.output_values.clear()
        if not self.silent:
            print(output)
        return output

    def take(self, item):
        self.issue('take '+item)
        self.inventory.append(item)

    def drop(self, item):
        self.issue('drop '+item)
        self.inventory.remove(item)
        

def main():
    program_input = parse_program_input(sys.stdin.read())
    game = Program(program_input)
    player = Player(game)
    player.play()
    

if __name__ == '__main__':
    main()
