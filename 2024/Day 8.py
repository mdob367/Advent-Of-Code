import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy


def parse_map(input_map):
    res = []
    for line in input_map.split('\n'):
        res.append(list(line))

    return res

def print_map(display_map):
    for line in display_map:
        print(''.join(line))


def in_map(pos, map):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])

def find_antennas(input_map):
    antennas = {}
    for i in range(len(input_map)):
        for j in range(len(input_map[0])):
            if input_map[i][j].isalnum():
                antennas[input_map[i][j]] = antennas.get(input_map[i][j], []) + [(i,j)]
    return antennas


def parse_input(input):
    input = parse_map(input)
    antennas = find_antennas(input)
    return input, antennas


def find_antinodes(puzz_input):
    input_map, antennas = parse_input(puzz_input)
    # Loop through every 2 pairs of antennas
    antinodes = []
    for antenna, locs in antennas.items():
        if len(locs)<2:
            continue
        for i in range(len(locs)):
            for j in range(i+1, len(locs)):
                x_dist = locs[i][0] - locs[j][0]
                y_dist = locs[i][1] - locs[j][1]
                gcd = math.gcd(x_dist, y_dist)
                x_dist //= gcd
                y_dist //= gcd
                option = locs[i][0], locs[i][1]
                while in_map(option, input_map):
                    antinodes.append(option)
                    option = option[0] + x_dist, option[1] + y_dist
                option = locs[j][0], locs[j][1]
                while in_map(option, input_map):
                    antinodes.append(option)
                    option = option[0] - x_dist, option[1] - y_dist
    return set(antinodes)


test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


real_input = get_input.get_input_file(8)
input_map = parse_input(real_input)[0]
antinodes = find_antinodes(real_input)
for anitnode in antinodes:
    input_map[anitnode[0]][anitnode[1]] = '#'
print_map(input_map)
# print(antinodes)
print(len(set(antinodes)))