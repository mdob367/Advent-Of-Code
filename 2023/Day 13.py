import numpy as np
import re
import math
import itertools
import requests

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/13/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

def parse(input):
    input = input.split('\n\n')
    input = np.array([np.array([list(line) for line in mp.split('\n')]) for mp in input])

    return input

def find_reflection(rocks):
    """ Find the reflection of the rocks in the map. A reflection is where all columns to the left of the reflection
     match the columns to the right of the reflection. """
    # Find the reflection
    for reflect_col in range(1, len(rocks[0])):
        # print(reflect_col, len(rocks[0]), reflect_col <= len(rocks[0])//2)
        if reflect_col <= len(rocks[0])//2:
            start_col = 0
            end_col = reflect_col*2
        else:
            start_col = reflect_col*2 - len(rocks[0])
            end_col = len(rocks[0])
        # print start_col, end_col
        # print(start_col, end_col)
        left = [line[start_col:reflect_col] for line in rocks]
        right = [line[reflect_col:end_col] for line in rocks]
        right = [line[::-1] for line in right]
        # # print left as string
        # print('left')
        # print('\n'.join([''.join(line) for line in left]))
        # # print right as string
        # print('right')
        # print('\n'.join([''.join(line) for line in right]))
        # print('\n\n')

        # compare arrays
        errors = 0
        for i in range(len(left)):
            for j in range(len(left[0])):
                if left[i][j] != right[i][j]:
                    errors += 1
        if errors == 1:
            return reflect_col

        
example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
# map_list = parse(get_input_file())
tot=0
# map_list = parse(example)

example2 = """##.#
#..#
##.#
##.#"""

map_list = parse(get_input_file())
# map_list = parse(example2)
for rock_map in map_list:
    print(rock_map)
    col_ref = find_reflection(rock_map)
    if col_ref:
        print(col_ref)
        tot+=col_ref
    # Rotate the map

    rock_map = np.rot90(np.array(rock_map))
    print(rock_map)
    row_ref = find_reflection(rock_map)
    if row_ref:
        print(row_ref)
        tot+=row_ref*100
print(tot)
    

