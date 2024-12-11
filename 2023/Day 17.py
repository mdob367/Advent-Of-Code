import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
import time
import functools
from bisect import insort_left

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__!r} executed in {(end_time - start_time):.4f}s")
        # print(f"{(end_time - start_time):.4f}s")
        return result
    return wrapper


def parse_map(heat_map):
    res = []
    for line in heat_map.split('\n'):
        int_line = [int(c) for c in line]
        res.append(int_line)

    return res

dir_map = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1), 'X': (0, 0)}
rt_angles = {'U': ('L', 'R'), 'D': ('R', 'L'), 'L': ('D', 'U'), 'R': ('U', 'D'), 'X': ('D', 'R')}

def poss_routes(curr_pos, curr_heat, min_dist=1, max_dist=3):
    poss = []
    new_i, new_j, dir, dist = curr_pos
    new_heat = curr_heat

    new_dir = dir
    travel = dir_map[dir]
    
    while True:
        dist += 1
        new_i, new_j = new_i + travel[0], new_j + travel[1]

        if new_i < 0 or new_j < 0 or new_i >= MAP_LEN[0] or new_j >= MAP_LEN[1]:
            break
        else:
            new_heat = new_heat + HEAT_MAP[new_i][new_j]

        if dist < min_dist:
            continue
        elif dist > max_dist:
            break
        else:
            poss.append((new_i, new_j, new_dir, dist, new_heat))

    for new_dir in rt_angles[dir[0]]:
        new_i, new_j, _, _ = curr_pos
        new_heat = curr_heat


        travel = dir_map[new_dir]
        dist = 0
        while True:
            dist += 1
            new_i, new_j = new_i + travel[0], new_j + travel[1]

            if new_i < 0 or new_j < 0 or new_i >= MAP_LEN[0] or new_j >= MAP_LEN[1]:
                break
            else:
                new_heat = new_heat + HEAT_MAP[new_i][new_j]

            if dist < min_dist:
                continue
            elif dist > max_dist:
                break
            else:
                poss.append((new_i, new_j, new_dir, dist, new_heat))

    return poss

@timeit
def search_map():
    start_time = time.time()
    cooling = {}
    current = (0, 0, 'X', 1)
    cooling[current] = 0
    min_dist = 4
    max_dist = 10

    poss = []
    interim_poss = poss_routes(current, cooling[current], min_dist, max_dist)
    for new_poss in interim_poss:
        if new_poss[2] != 'X':
            poss.append(new_poss)

    poss.sort(key=lambda x: x[3], reverse=True)

    best_yet = math.inf
    farthest = (0,0,0)

    while poss:
        next_pos = poss.pop()
        current = next_pos[:4]
        cool = next_pos[4]


        if cooling.get(current, math.inf) < cool or cool > best_yet:
            continue
        else:
            cooling[current] = cool
            i, j = current[0], current[1]
            if i+j > farthest[0]:
                farthest = (i+j, i, j)
            if len(cooling) % 100 == 0:
                print(len(cooling), "Out of", MAP_LEN[0]*MAP_LEN[1]*12, "Best:", best_yet, "Farthest:", farthest[1:], "Possibilities:", len(poss), "Time:", f'{time.time()-start_time:.0f}s')
            for new_poss in poss_routes(current, cool, min_dist, max_dist):
                if cooling.get(new_poss[:4], math.inf) <= new_poss[4]:
                    continue
                else:
                   cooling[new_poss[:4]] = new_poss[4]
                   insort_by_key(poss, new_poss, 4)
            if current[0] == MAP_LEN[0]-1 and current[1] == MAP_LEN[1]-1:
                if cool < best_yet:
                    best_yet = cool
                    print("New Best", best_yet, current)
    return best_yet, cooling

def insort_by_key(lst, item, key_index):
    left = 0
    right = len(lst)

    while left < right:
        mid = (left + right) // 2
        if lst[mid][key_index] > item[key_index]: 
            left = mid + 1
        else:
            right = mid

    lst.insert(left, item)


example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""



# HEAT_MAP = parse_map(example)
HEAT_MAP = parse_map(get_input.get_input_file(17))

MAP_LEN = len(HEAT_MAP), len(HEAT_MAP[0])
print(MAP_LEN)

best_route = search_map()

best_yet, cooling = best_route

print(best_yet)

def disp_cooling(cooling):
    max_cool = 0
    best_cool = {}
    for i, j, dir, dist in cooling:
        if cooling[(i, j, dir, dist)] < best_cool.get((i, j), math.inf):
            best_cool[(i, j)] = cooling[(i, j, dir, dist)]
        if cooling[(i, j, dir, dist)] > max_cool:
            max_cool = cooling[(i, j, dir, dist)]

    divisor = 10**(int(math.log(max_cool+1, 10))-1)

    for i in range(len(HEAT_MAP)):
        for j in range(len(HEAT_MAP[0])):
            if (i, j) in best_cool:
                print('', int(best_cool[(i, j)]/divisor), end='')
            else:
                print('','.', end='')
        print('\n')

# disp_cooling(cooling)