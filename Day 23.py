import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time

def parse_hiking_map(hiking_map):
    hiking_map = hiking_map.split('\n')
    hiking_map = [list(line) for line in hiking_map]
    start = (1, hiking_map[0].index('.'))
    end = (len(hiking_map) - 1, hiking_map[-1].index('.'))
    # Add border of #
    hiking_map.insert(0, ['#'] * len(hiking_map[0]))
    hiking_map.append(['#'] * len(hiking_map[0]))
    # hiking_map = np.array(hiking_map)
    return hiking_map, start, end


example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

# hiking_map, start, end = parse_hiking_map(get_input.get_input_file(23))
hiking_map, start, end = parse_hiking_map(example)

def find_path(hiking_map, start):
    path = {start: []}
    spots = [start]
    while spots:
        curr_spot = spots.pop()
        poss_dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if hiking_map[curr_spot[0]][curr_spot[1]] == '<':
            poss_dir = [(0, -1)]
        elif hiking_map[curr_spot[0]][curr_spot[1]] == '>':
            poss_dir = [(0, 1)]
        elif hiking_map[curr_spot[0]][curr_spot[1]] == 'v':
            poss_dir = [(1, 0)]

        for dir in poss_dir:
            new_spot = (curr_spot[0] + dir[0], curr_spot[1] + dir[1])
            # if new_spot[0] < 0 or new_spot[1] < 0 or new_spot[0] >= len(hiking_map) or new_spot[1] >= len(hiking_map[0]):
            #     continue
            if hiking_map[new_spot[0]][new_spot[1]] == '#':
                continue
            if new_spot in path[curr_spot]:
                continue
            if new_spot in path:
                if (len(path[curr_spot]) + 1) > len(path[new_spot]):
                    path[new_spot] = path[curr_spot] + [curr_spot]
                    spots.append(new_spot)
                else:
                    continue
            else:
                path[new_spot] = path[curr_spot] + [curr_spot]
                spots.append(new_spot)
        spots.sort(key=lambda x: len(path[x]))
    # print(path[end])
    return path[end]


def find_longer_path(hiking_map, start):
    path = {start: []}
    spots = [start]
    while spots:
        curr_spot = spots.pop()
            
        poss_dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if hiking_map[curr_spot[0]][curr_spot[1]] == '<':
            poss_dir = [(0, -1)]
        elif hiking_map[curr_spot[0]][curr_spot[1]] == '>':
            poss_dir = [(0, 1)]
        elif hiking_map[curr_spot[0]][curr_spot[1]] == 'v':
            poss_dir = [(1, 0)]

        for dir in poss_dir:
            new_spot = (curr_spot[0] + dir[0], curr_spot[1] + dir[1])
            # if new_spot[0] < 0 or new_spot[1] < 0 or new_spot[0] >= len(hiking_map) or new_spot[1] >= len(hiking_map[0]):
            #     continue
            if hiking_map[new_spot[0]][new_spot[1]] == '#':
                continue
            if new_spot in path[curr_spot]:
                continue
            if new_spot in path:
                if (len(path[curr_spot]) + 1) > len(path[new_spot]):
                    path[new_spot] = path[curr_spot] + [curr_spot]
                    spots.append(new_spot)
                else:
                    continue
            else:
                path[new_spot] = path[curr_spot] + [curr_spot]
                spots.append(new_spot)
        spots.sort(key=lambda x: len(path[x]))
    # print(path[end])
    return path[end]

start_time = time.time()
for _ in range(1000):
    longest_path = find_path(hiking_map, start)
print(len(longest_path)+1)
# print([len(x)-1 for x in long_paths])
# for spot in long_paths[0]:
    # hiking_map[spot[0]][spot[1]] = 'O'
# dot_count = 0
# for line in hiking_map:
#     print(''.join(line))
#     dot_count += line.count('.')
# print(dot_count)
print(time.time() - start_time)