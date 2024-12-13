import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy


def parse_map(input_map):
    res = []
    if input_map[0]=='\n':
        input_map = input_map[1:]
    for line in input_map.split('\n'):
        res.append([int(val) for val in line])

    return res

def print_map(display_map):
    for line in display_map:
        print(''.join([str(v) for v in line]))


def in_map(pos, map):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])


def find_trailpoints(input_map):
    trailheads = []
    trailpeaks = []
    for i in range(len(input_map)):
        for j in range(len(input_map[0])):
            if input_map[i][j]==0:
                trailheads.append((i,j))
            elif input_map[i][j]==9:
                trailpeaks.append((i,j))
    return trailheads, trailpeaks


def find_paths(input_map, trailheads):
    poss_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    found_routes = []
    trails = [[t] for t in trailheads]
    while trails:
        next_steps = []

        for trail in trails:
            i, j = trail[-1]
            height = input_map[i][j]
            if height==9:
                found_routes.append(trail.copy())
                # known_paths.extend(trail)
            for dir in poss_dirs:
                if in_map((i+dir[0], j+dir[1]), input_map) and input_map[i+dir[0]][j+dir[1]]==height+1:
                    pos = (i+dir[0], j+dir[1])
                    next_steps.append(trail.copy() + [pos])
        trails = next_steps

    return found_routes


def find_all_paths(input_map):
    trailheads, trailpeaks = find_trailpoints(input_map)
    return find_paths(input_map, trailheads)


def cum_score(input_map):
    paths = find_all_paths(input_map)
    print(len(paths))
    pairs = []
    for path in paths:
        pairs.append((path[0], path[-1]))
    return len(set(pairs))


test_input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


real_input = get_input.get_input_file(10)
input_map = parse_map(real_input)
print_map(input_map)
# print(antinodes)
print(cum_score(input_map))
# print(*find_all_paths(input_map), sep='\n')