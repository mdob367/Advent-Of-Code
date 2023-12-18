import numpy as np
import re
import math
import itertools
import requests

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/18/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

def parse_input(input):
    input = input.split('\n')
    input = [line.split() for line in input]
    return input

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

def dig_trench(input, size=1000):
    input = parse_input(input)
    trench_map = [['.' for i in range(size)] for j in range(size)]

    loc = [size//2,size//2]
    prev_dir = input[-1][0]
    input[-1][1] = int(input[-1][1])-1
    for line in input:
        print(loc, line)
        dir = line[0]
        dist = int(line[1])
        if dir == 'U':
            if prev_dir == 'R':
                trench_map[loc[0]][loc[1]] = 'J'
            elif prev_dir == 'L':
                trench_map[loc[0]][loc[1]] = 'L'
            for i in range(dist):
                loc[0] -= 1
                trench_map[loc[0]][loc[1]] = '|'
        elif dir == 'D':
            if prev_dir == 'R':
                trench_map[loc[0]][loc[1]] = '7'
            elif prev_dir == 'L':
                trench_map[loc[0]][loc[1]] = 'F'
            for i in range(dist):
                loc[0] += 1
                trench_map[loc[0]][loc[1]] = '|'
        elif dir == 'R':
            if prev_dir == 'U':
                trench_map[loc[0]][loc[1]] = 'F'
            elif prev_dir == 'D':
                trench_map[loc[0]][loc[1]] = 'L'

            for i in range(dist):
                loc[1] += 1
                trench_map[loc[0]][loc[1]] = '-'
        elif dir == 'L':
            if prev_dir == 'U':
                trench_map[loc[0]][loc[1]] = '7'
            elif prev_dir == 'D':
                trench_map[loc[0]][loc[1]] = 'J'
            for i in range(dist):
                loc[1] -= 1
                trench_map[loc[0]][loc[1]] = '-'
        else:
            print('Error')
            return
        prev_dir = dir
    
    loc = [size//2,size//2]
    return trench_map

def fill_interior(trench_map):
    inside=[]
    for line in range(len(trench_map)):
        loop_count = {'F': 0, "L": 0, "J": 0, "7": 0, "|": 0}
        for char in range(len(trench_map[line])):
            node = (line, char)
            node_char = trench_map[node[0]][node[1]]
            if node_char != '.' and node_char != '-':
                loop_count[node_char] += 1
            net_crossings = min(loop_count['F'], loop_count['J']) + min(loop_count['7'], loop_count['L']) + loop_count['|']
            if net_crossings % 2 == 1:
                if trench_map[node[0]][node[1]] == '.':
                    trench_map[node[0]][node[1]] = '#'
    return trench_map

trench_map = dig_trench(get_input_file(), 1000)
print('\n'.join([''.join(line) for line in trench_map]))
trench_map = fill_interior(trench_map)
print('\n'.join([''.join(line) for line in trench_map]))
# Count non-'.' in trench_map
count = 0
for line in trench_map:
    for char in line:
        if char != '.':
            count += 1
print(count)
