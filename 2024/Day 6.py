import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy


def parse_map(input_map, start_char):
    res = []
    for i, line in enumerate(input_map.split('\n')):
        if start_char in line:
            start = (i, line.index(start_char))
            line = line.replace(start_char, '.')
        res.append(list(line))

    return res, start

dir_dict = {(-1, 0): ['^', '>'], (1, 0): ['v', '<'], (0, -1): ['<', '^'], (0, 1): ['>', 'v']}

def in_map(pos, map):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])

def in_path(pos, dir, map):
    while in_map(pos, map):
        if map[pos[0]][pos[1]] == dir_dict[dir][1]:
            return True
        pos = (pos[0] + dir[0], pos[1] + dir[1])

def turn_dir(dir):
    return (dir[1], -dir[0])

def find_loops(guard_map, start_pos, start_dir):
    pos = start_pos
    dir = start_dir

    loop_blocks = []
    counter = 0

    while True:
        # counter += 1
        # if counter % 10 == 0:
        #     print(counter, '\n\n\n')
        #     print_map(guard_map)
        guard_map[pos[0]][pos[1]] = 'X'
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])

        if not in_map(next_pos, guard_map):
            break
        if guard_map[next_pos[0]][next_pos[1]] == '#':
            dir = turn_dir(dir)
        else:
            # Check if we can make a loop
            if next_pos not in loop_blocks:
                loop_guard_map = deepcopy(guard_map)