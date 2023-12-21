import numpy as np
import re
import math
import itertools
import get_input

example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def parse_map(mirr_map):
    mirr_map = mirr_map.split('\n')
    mirr_map = [list(line) for line in mirr_map]
    # mirr_map = np.array(mirr_map)
    return mirr_map


def next_spot(mirr_map, current):
    i, j, dir = current
    lens = mirr_map[i][j]
    m, n = len(mirr_map), len(mirr_map[0])
    next_spot = []
    if lens == '.':
        if dir == 'down':
            i += 1
        elif dir == 'up':
            i -= 1
        elif dir == 'left':
            j -= 1
        elif dir == 'right':
            j += 1
    elif lens == '|':
        if dir == 'down':
            i += 1
        elif dir == 'up':
            i -= 1
        elif dir == 'left' or dir == 'right':
            next_spot = [(i-1, j, 'up'), (i+1, j, 'down')]
    elif lens == '-':
        if dir == 'left':
            j -= 1
        elif dir == 'right':
            j += 1
        elif dir == 'up' or dir == 'down':
            next_spot = [(i, j-1, 'left'), (i, j+1, 'right')]
    elif lens == '/':
        if dir == 'up':
            j += 1
            dir = 'right'
        elif dir == 'right':
            i -= 1
            dir = 'up'
        elif dir == 'down':
            j -= 1
            dir = 'left'
        elif dir == 'left':
            i += 1
            dir = 'down'
    elif lens == '\\':
        if dir == 'up':
            j -= 1
            dir = 'left'
        elif dir == 'right':
            i += 1
            dir = 'down'
        elif dir == 'down':
            j += 1
            dir = 'right'
        elif dir == 'left':
            i -= 1
            dir = 'up'
    if not next_spot:
        next_spot = [(i, j, dir)]
    for spt in next_spot:
        if spt[0] < 0 or spt[0] >= m or spt[1] < 0 or spt[1] >= n:
            next_spot.remove(spt)
    return next_spot


def energize(str_map):
    mirr_map = parse_map(str_map)
    energized = []
    spot = [(0, 0, 'right')]
    while spot:
        next_spot_list = []
        for spt in spot:
            print(spt, mirr_map[spt[0]][spt[1]])
            if spt in energized:
                continue
            else:
                energized += [spt]
                next_spot_list += next_spot(mirr_map, spt)
        spot = next_spot_list
    energized = set([(i, j) for i, j, _ in energized])
    return len(energized)
print(energize(get_input.get_input_file(16)))