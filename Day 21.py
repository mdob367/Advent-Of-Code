import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time


def parse_map(garden_map):
    res = []
    for i, line in enumerate(garden_map.split('\n')):
        if 'S' in line:
            start = (i, line.index('S'))
            line = line.replace('S', '.')
        res.append(list(line))

    return res, start


example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

def go_for_a_walk(garden_map, start, max_steps):
    garden_map = np.array(garden_map)
    steps_map = {start: 0}
    spots = [start]
    reachable = set(start)
    height, width = garden_map.shape
    shown = []
    while spots:
        curr_spot = spots.pop()
        curr_steps = steps_map[curr_spot]
        if len(steps_map) % 10000 == 0 and len(steps_map) not in shown:
            print(len(steps_map))
            shown.append(len(steps_map))
        if curr_steps > max_steps:
            continue
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]: 
            new_spot = (curr_spot[0] + dir[0], curr_spot[1] + dir[1])
            new_map_loc = (new_spot[0] % height, new_spot[1] % width)
            if garden_map[new_map_loc] == '#':
                continue
            else:
                if new_spot not in steps_map:
                    steps_map[new_spot] = curr_steps + 1
                    spots.append(new_spot)
                    if (steps_map[new_spot] - max_steps) % 2 == 0:
                        # append to set
                        reachable.add(new_spot)
                elif curr_steps + 1 < steps_map[new_spot]:
                    steps_map[new_spot] = curr_steps + 1
                    spots.append(new_spot)
                    if (steps_map[new_spot] - max_steps) % 2 == 0:
                        reachable.add(new_spot)

    # print(garden_map)
    # print(steps_map)
    # Count points with steps less than max_steps
    return len(reachable)


# garden_map, start = parse_map(get_input.get_input_file(21))
garden_map, start = parse_map(example)

print(go_for_a_walk(garden_map, start, 1000))