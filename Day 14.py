import numpy as np
import re
import math
import itertools
import requests
from functools import lru_cache
import time
import functools
import cProfile
import pstats



def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/14/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt


def parse_inp_str(input_str):
    # Convert to numpy array
    output = input_str.split('\n')
    output = [list(line) for line in output]
    output = np.array(output)
    return output

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

def process_input(source='ex'):
    if source == 'ex':
        input = example
    else:
        input = get_input_file()
    input = parse_inp_str(input)
    return input

example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def move_rocks(rock_map, dir):
    # Convert tuple to list for easier manipulation
    rock_map_list = list(map(list, rock_map))

    if dir in ['U', 'D']:
        len_rock_map = len(rock_map_list[0])
    elif dir in ['L', 'R']:
        len_rock_map = len(rock_map_list)

    for i in range(len_rock_map):
        if dir in ['U', 'D']:
            col_arr = [row[i] for row in rock_map_list]
        elif dir in ['L', 'R']:
            col_arr = rock_map_list[i]

        if dir in ['D', 'R']:
            col_arr = col_arr[::-1]

        col_arr = move_col(''.join(col_arr))
        if dir in ['D', 'R']:
            col_arr = col_arr[::-1]

        if dir in ['U', 'D']:
            for j, val in enumerate(col_arr):
                rock_map_list[j][i] = val
        elif dir in ['L', 'R']:
            rock_map_list[i] = list(col_arr)

    # Convert list back to tuple
    rock_map = array_to_tuple(rock_map_list)

    return rock_map


@lru_cache(maxsize=None)
def move_col(col_arr):
    col_arr = col_arr.split('#')
    out_arr = []

    for segment in col_arr:

        out_arr.extend(sort_seg(segment))
        out_arr.append('#')

    # Remove the last '#' added by the loop
    out_arr.pop()

    return out_arr

@lru_cache(maxsize=None)
def sort_seg(segment):
    o_count = segment.count('O')
    dot_count = len(segment) - o_count
    return ['O'] * o_count + ['.'] * dot_count

def calc_weight(rock_map):
    weight = 0
    for i_row in range(len(rock_map)):
        # Count Os in row
        count = list(rock_map[i_row]).count('O')
        weight += count * (len(rock_map)-i_row)
    return weight

@timeit
def spin(rock_map, spin_count):
    rock_map = array_to_tuple(rock_map)
    seen_before = {}
    i=0
    while i< spin_count:
        print(i)
        if rock_map in seen_before:
            print("Seen it!", i, seen_before[rock_map], spin_count)
            gap = i - seen_before[rock_map]
            to_go = spin_count - i
            i = (to_go // gap)*gap + i
            print(i, seen_before[rock_map], spin_count, to_go, gap)
            seen_before = {}
        seen_before[rock_map] = i        
        rock_map = move_rocks(rock_map, 'U')
        rock_map = move_rocks(rock_map, 'L')
        rock_map = move_rocks(rock_map, 'D')
        rock_map = move_rocks(rock_map, 'R')
        i+=1
    return rock_map


def array_to_tuple(arr):
    return tuple(tuple(row) for row in arr)


def run_model(profile='cp'):
    rock_map = process_input('')

    if profile == 'cp':
        # Create a Profile object
        profiler = cProfile.Profile()
        profiler.enable()




        # print(move_rocks(rock_map))
        print(spin(rock_map, 100000000))
        # print(calc_weight(move_rocks('file')))

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumulative')
        stats.print_stats()
    else:
        # print(move_rocks(rock_map))
        rock_map = spin(rock_map, 1000000000)
        print(calc_weight(rock_map))

run_model('')
