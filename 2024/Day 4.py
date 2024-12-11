import numpy as np
import re
import math
import itertools
import get_input


def parse_input(input):
    input = input.split('\n')
    input = np.array([list(line) for line in input])
    return input

def add_borders(map):
    # Add rows of '.' to the top and bottom
    top_bottom_border = np.full((1, map.shape[1]), '.')
    new_map = np.vstack([top_bottom_border, map, top_bottom_border])

    # Add columns of '.' to the left and right
    side_border = np.full((new_map.shape[0], 1), '.')
    new_map = np.hstack([side_border, new_map, side_border])

    return new_map


def find_xmas(word_grid):
    xmases = set()
    for i in range(1, word_grid.shape[0] - 1):
        for j in range(1, word_grid.shape[1] - 1):
            if word_grid[i][j] == 'X':
                for direction in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                    if word_grid[i + direction[0]][j + direction[1]] == 'M' and word_grid[i + 2 * direction[0]][j + 2 * direction[1]] == 'A' and word_grid[i + 3 * direction[0]][j + 3 * direction[1]] == 'S':
                        xmases.add((i, j, direction))
    return xmases

def find_Xmas(word_grid):
    xmases = set()
    for i in range(1, word_grid.shape[0] - 1):
        for j in range(1, word_grid.shape[1] - 1):
            if word_grid[i][j] == 'A':
                x_let = []
                for direction_pair in [[(1, 1), (-1, -1)], [(1, -1), (-1, 1)]]:
                    x_let.append(word_grid[i + direction_pair[0][0]][j + direction_pair[0][1]] + word_grid[i + direction_pair[1][0]][j + direction_pair[1][1]])
                if (x_let[0] == 'MS' or x_let[0] == 'SM') and (x_let[1] == 'MS' or x_let[1] == 'SM'):
                    xmases.add((i, j))
    return xmases

test_input ="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

# puzz_input = (parse_input(test_input))
# puzz_input = (parse_input(get_input.get_input_file(2)))
# print(puzz_input)

puzz_input = test_input
puzz_input = get_input.get_input_file(4)
#
puzz_input = add_borders(parse_input(puzz_input))
# puzz_input = parse_input(puzz_input)
print(len(find_Xmas(puzz_input)))
