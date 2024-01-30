import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time
from copy import deepcopy

def parse_hiking_map(hiking_map):
    hiking_map = hiking_map.replace('>', '.')
    hiking_map = hiking_map.replace('<', '.')
    hiking_map = hiking_map.replace('v', '.')
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


def find_decisions(hiking_map):
    decisions = {2: 0, 3: 0}
    poss_dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(len(hiking_map)):
        for j in range(len(hiking_map[0])):
            if hiking_map[i][j] != '.':
                continue
            next_count = 0
            for dir in poss_dir:
                new_spot = (i + dir[0], j + dir[1])
                if hiking_map[new_spot[0]][new_spot[1]] == '.':
                    next_count += 1
            if next_count > 2:
                decisions[next_count-1] += 1
    return decisions

def remove_dupes(paths):
    start_len = len(paths)
    checked = {}
    deduped_paths = []
    for path, path_len in paths:
        start, end = path[0], path[-1]
        if (start, end) in checked:
            continue
        else:
            checked[(start, end)] = [set(path)]
            deduped_paths.append((path, path_len))
        for path2, path_len2 in paths:
            if end != path2[-1]:
                continue
            if set(path2) in checked[(start, end)]:
                continue
            else:
                checked[(start, end)].append(set(path2))
                deduped_paths.append((path2, path_len2))
    end_len = len(deduped_paths)
    print('removed', start_len - end_len)
    if end_len != start_len:
        print('found dupes')
        exit()
    return deduped_paths

def find_longer_path(hiking_map, start, end):
    paths = [([start], 1)]
    best_path = ([start], 1)
    final_count = 0
    while paths:
        removed = 0

        new_paths = []
        for path_and_len in paths:
            path, path_len = path_and_len
            spot = path[-1]
            if spot == end:
                final_count += 1
                if path_len > best_path[1]:
                    best_path = path_and_len
                    print('new largest', best_path[1])
                    # display_map(best_path[0])
                    continue
            poss_dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            next_spots = [[]]
            one_dir_path = []
            while len(next_spots) == 1:
                removed -= 1
                next_spots = []
                for dir in poss_dir:
                    new_spot = (spot[0] + dir[0], spot[1] + dir[1])
                    if hiking_map[new_spot[0]][new_spot[1]] == '#':
                        continue
                    if new_spot == end:
                        path = path[:-1] + [spot, new_spot]
                        new_paths.append((path, path_len + 1))
                        continue
                    if new_spot in path or new_spot in one_dir_path:
                        removed += 1
                        continue
                    next_spots.append(new_spot)
                if len(next_spots) == 1:
                    one_dir_path = [spot, next_spots[0]]
                    spot = next_spots[0]
                    path_len += 1
                else:
                    for new_spot in next_spots:
                        new_path = path + [spot, new_spot]
                        new_paths.append((new_path, path_len + 1))
        # paths = remove_dupes(new_paths)
        paths = new_paths
        # print(len(paths), len(new_paths))
        # if len(paths)==38:
        #     for path in paths:
        #         display_map(path)
        # if len(paths) %100 ==0:
        print('paths', len(paths), 'reached end', final_count, 'removed', removed)


    return best_path

def display_map(path):
    display_map = deepcopy(hiking_map)
    asdf = 0
    for spot in path[:-1]:
        display_map[spot[0]][spot[1]] = 'O'
        asdf += 1
    spot = path[-1]
    display_map[spot[0]][spot[1]] = '*'
    asdf += 1
    print(asdf)
    dot_count = 0
    o_ct = 0
    for line in display_map:
        print(''.join(line))
        dot_count += line.count('.')
        o_ct += line.count('O')
    print('dots', dot_count)
    print('Os', o_ct)

hiking_map, start, end = parse_hiking_map(get_input.get_input_file(23))
# hiking_map, start, end = parse_hiking_map(example)

start_time = time.time()
for _ in range(1):
    longest_path, longest_length = find_longer_path(hiking_map, start, end)
    decisions = find_decisions(hiking_map)
    print('decisions', len(decisions), decisions)
    display_map(longest_path)
    print('Answer is', longest_length)
    print('Answer is not 4674')
print(time.time() - start_time)


