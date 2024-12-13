import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy


def parse_map(input_map):
    res = []
    if input_map[0]=='\n':
        input_map = input_map[1:]
    for line in input_map.split('\n'):
        res.append([val for val in line])

    return res

def print_map(display_map):
    for line in display_map:
        print(''.join([str(v) for v in line]))


def in_map(pos, map):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])


def find_region(plot_map):
    regions = []
    for i in range(len(plot_map)):
        for j in range(len(plot_map[0])):
            # print_map(plot_map)
            found_region = []
            searching = []
            region = plot_map[i][j]
            if region !='.':
                searching = [(i,j)]
            while searching:
                pos = searching.pop()
                found_region.append(pos)
                plot_map[pos[0]][pos[1]] = '.'

                for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_spot = (pos[0]+dir[0], pos[1]+dir[1])
                    if in_map(next_spot, plot_map) and plot_map[next_spot[0]][next_spot[1]] == region and next_spot not in found_region and next_spot not in searching:
                        searching.append(next_spot)
            if found_region:
                regions.append(found_region)
    return regions


def calc_perim(region, input_map):
    perim = 0
    for pos in region:
        borders = 4
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if in_map(next_pos, input_map) and next_pos in region:
                borders -= 1
        perim += borders
    return perim


def needs_side(border_pos, region, map):
    if not in_map(border_pos, map):
        return True
    if border_pos not in region:
        return True
    return False


def calc_sides(region, input_map):
    side_ct = 0
    sides_covered = {pos: {'U': False, 'D': False, 'L': False, 'R': False} for pos in region}
    side_dir = {'U': [(-1, 0), [(0,-1), (0, 1)]], 
                'D': [(1, 0), [(0,-1), (0, 1)]], 
                'L': [(0, -1), [(-1, 0), (1, 0)]], 
                'R': [(0, 1), [(-1, 0), (1, 0)]]}
    for pos in region:
        for sd in side_dir:
            border_dir = side_dir[sd][0]
            dir_checks = side_dir[sd][1]
            if sides_covered[pos][sd]:
                # Already accounted for
                continue
            next_pos = (pos[0]+border_dir[0], pos[1]+border_dir[1])
            if not needs_side(next_pos, region, input_map):
                # No side needed since still in region
                sides_covered[pos][sd] = True
            else:
                side_ct += 1
                sides_covered[pos][sd] = True
                # Look along border
                for dir in dir_checks:
                    next_pos = (pos[0]+dir[0], pos[1]+dir[1])
                    border_pos = (next_pos[0]+border_dir[0], next_pos[1]+border_dir[1])
                    while next_pos in region and needs_side(border_pos, region, input_map):
                        sides_covered[next_pos][sd] = True
                        next_pos = (next_pos[0]+dir[0], next_pos[1]+dir[1])
                        border_pos = (next_pos[0]+border_dir[0], next_pos[1]+border_dir[1])
    return side_ct

def calc_cost(input_map):
    regions = find_region(input_map)
    # return sum([calc_perim(region, input_map)*len(region) for region in regions])
    return sum([calc_sides(region, input_map)*len(region) for region in regions])

test_input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

# test_input 

real_input = get_input.get_input_file(12)
input_map = parse_map(real_input)
# print_map(input_map)
print(calc_cost(input_map))
# print(antinodes)
# print(*find_all_paths(input_map), sep='\n')