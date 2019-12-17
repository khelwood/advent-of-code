#!/usr/bin/env python3

import sys

sys.path.append('..')

from point import Point
from intcode import Program, parse_program_input

ORIGIN = Point(0, 0)
NORTH = Point(0, -1)
SOUTH = Point(0, 1)
EAST = Point(1, 0)
WEST = Point(-1, 0)
DIRECTIONS = (NORTH, SOUTH, EAST, WEST)
DIR_NUMBER = { NORTH: 1, SOUTH:2, EAST: 3, WEST: 4}

WALL_S = '#'
SPACE_S = '.'
GUY_S = '*'
TARGET_S = 'T'
TARGET_GUY_S = '@'

BLOCKED_N = 0
MOVED_N = 1
FOUND_N = 2

def adjacency(pos):
    for d in DIRECTIONS:
        yield (pos+d)

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# First direction: west
# Target: (-16, -12)

class Maze:
    def __init__(self):
        self.p0 = ORIGIN
        self.p1 = ORIGIN
        self.layout = {}
    def __getitem__(self, index):
        return self.layout.get(index, ' ')
    def __setitem__(self, index, value):
        self.p0 = Point.min(self.p0, index)
        self.p1 = Point.max(self.p1, index)
        self.layout[index] = value
    def unexplored_dir(self, pos):
        return next((d for d in DIRECTIONS if (pos+d) not in self.layout), None)
    def nearest_unexplored(self, pos):
        nearest = None
        nearest_distance = None
        for k,v in self.layout.items():
            if v==WALL_S:
                continue
            d = manhattan(k, pos)
            if nearest_distance is not None and nearest_distance <= d:
                continue
            if self.unexplored_dir(k) is None:
                continue
            nearest_distance = d
            nearest = k
        return nearest
    def render(self, guy, target):
        x0, y0 = self.p0
        x1, y1 = self.p1
        guystring = TARGET_GUY_S if guy==target else GUY_S
        for y in range(y0, y1+1):
            for x in range(x0, x1+1):
                print(guystring if (x,y)==guy else 'S' if (x,y)==ORIGIN
                          else self[x,y], end='')
            print()

class Director:
    def __init__(self, program):
        self.guy = ORIGIN
        self.maze = Maze()
        self.steps = {ORIGIN: 0}
        self.target = None
        self.program = program
        self.direction = None
        self.route = None
        program.input_func = self.prog_input
        program.output_func = self.prog_output
    def prog_input(self):
        self.direction = d = self.next_direction()
        return DIR_NUMBER[d]
    def prog_output(self, value):
        dest = self.guy + self.direction
        if value==BLOCKED_N:
            self.maze[dest] = WALL_S
            return
        if value==FOUND_N:
            new_value = TARGET_S
            self.target = dest
        else:
            new_value = SPACE_S
        self.maze[dest] = new_value
        self.update_steps(dest)
        self.guy = dest
    def next_direction(self):
        guy = self.guy
        if self.route:
            return self.route.pop(0) - guy
        maze = self.maze
        d = maze.unexplored_dir(guy)
        if d is not None:
            return d
        dest = maze.nearest_unexplored(guy)
        if dest is None:
            raise StopIteration("Out of moves")
        self.route = route = plot_route(self.steps, guy, dest)
        return route.pop(0) - guy
    def update_steps(self, pos):
        least_steps = self.steps.get(pos)
        for adj in adjacency(pos):
            s = self.steps.get(adj)
            if s is None:
                continue
            s += 1
            if least_steps is None or s < least_steps:
                least_steps = s
        self.steps[pos] = least_steps
        adj_steps = least_steps + 1
        for adj in adjacency(pos):
            if self.steps.get(adj, 0) > adj_steps:
                self.steps[adj] = adj_steps
    def play(self):
        self.program.execute()
    def render(self):
        return self.maze.render(self.guy, self.target)
    def flood_steps(self, start):
        next_steps = [start]
        reachable = self.steps
        steps = {}
        count = 0
        while next_steps:
            current_steps = next_steps
            next_steps = []
            for pos in current_steps:
                steps[pos] = count
                for adj in adjacency(pos):
                    if adj in reachable and adj not in steps:
                        next_steps.append(adj)
            count += 1
        self.steps = steps

def plot_route(steps, src, dest):
    if manhattan(src, dest)==1:
        return [dest]
    from_dest = route_to_origin(steps, dest)
    try:
        si = from_dest.index(src)
        return from_dest[si-1::-1] + [dest]
    except ValueError:
        pass
    from_src = route_to_origin(steps, src)
    try:
        di = from_src.index(dest)
        return from_src[:di+1]
    except ValueError:
        pass
    return from_src + from_dest[-2::-1] + [dest]

def route_to_origin(steps, start, BIG_NUMBER=(1<<31)):
    route = []
    pos = start
    def adj_key(adj):
        return steps.get(adj, BIG_NUMBER)
    while pos != ORIGIN:
        pos = min(adjacency(pos), key=adj_key)
        route.append(pos)
    return route

def main():
    prog_input = parse_program_input(sys.stdin.read().strip())
    program = Program(prog_input)
    game = Director(program)
    try:
        game.play()
    except StopIteration as e:
        print(e)
    game.render()
    print("Distance to target:", game.steps[game.target])
    game.flood_steps(game.target)
    print("Time to fill with oxygen:", max(game.steps.values()))

if __name__ == '__main__':
    main()
