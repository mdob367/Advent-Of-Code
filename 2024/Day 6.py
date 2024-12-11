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
                loop_guard_map[next_pos[0]][next_pos[1]] = '#'
                change_dir = turn_dir(dir)
                if in_loop(loop_guard_map, start_pos, start_dir):
                    loop_blocks.append(next_pos)
                    print('current length:', len(loop_blocks))
                    # if len(loop_blocks) == 11:
                        # print_map(guard_map)
                    # guard_map[next_pos[0]][next_pos[1]] = 'O'
                    # print('\n\nLoop found at:', next_pos)
                    # print_map(guard_map)
                    # guard_map[next_pos[0]][next_pos[1]] = '#'
            pos = next_pos
 
    return loop_blocks


def in_loop(loop_guard_map, start_pos, start_dir):
    pos = start_pos
    dir = start_dir
    new_turn = [(pos, dir)]
    new_turn = []

    counter = 0
    while True:
        if counter >10:
            new_turn.append((pos, dir))
        counter += 1
        if counter % 1000000 == 0:
            print('error', new_turn)
            print_map(loop_guard_map)
            exit()

        loop_guard_map[pos[0]][pos[1]] = dir_dict[dir][0]
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])

        if not in_map(next_pos, loop_guard_map):
            return False
        if loop_guard_map[next_pos[0]][next_pos[1]] == '#':
            dir = (dir[1], -dir[0])
        else:
            pos = next_pos
        
        if (pos, dir) in new_turn:
            return True

 
    return False


def walk_map(loop_guard_map, start_pos, start_dir):

    pos = start_pos
    dir = start_dir

    while True:
        loop_guard_map[pos[0]][pos[1]] = 'X'
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])

        if not in_map(next_pos, loop_guard_map):
            break
        if loop_guard_map[next_pos[0]][next_pos[1]] == '#':
            dir = (dir[1], -dir[0])
        else:
            pos = next_pos
 
    return guard_map


def print_map(display_map):
    for line in display_map:
        print(''.join(line))


def count_guarded(guard_map):
    count = 0
    for line in guard_map:
        count += line.count('#') + line.count('.')
    return len(guard_map)**2 - count

def count_char(guard_map, ct_char):
    count = 0
    for line in guard_map:
        count += line.count(ct_char)
    return count

test_input ="""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

puzz_input = get_input.get_input_file(6)
# puzz_input = test_input

guard_map, start = parse_map(puzz_input, '^')
# guard_map = walk_map(guard_map, start, (-1, 0))
print_map(guard_map)
print(count_guarded(guard_map)) # Part 1
loops = find_loops(guard_map, start, (-1, 0))
print(loops)
print(len(loops))
print(len(set(loops)))