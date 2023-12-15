import numpy as np
import re
import math
import itertools
import requests

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/11/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

def parse_image(image):
    image = image.split('\n')
    image = [list(line) for line in image]
    image = np.array(image)
    return image

def expand(image):
    blanks = {'col': [], 'row': []}
    for i, line in enumerate(image):
        if all([c == '.' for c in line]):
            blanks['row'].append(i)
    # Rotate
    image = np.rot90(image, 3)
    image = np.array(image)
    for i, line in enumerate(image):
        if all([c == '.' for c in line]):
            blanks['col'].append(i)

    #Rotate back the other way
    # image = np.rot90(image, 3)

    return blanks

def number_galaxies(image):
    galaxy = 0
    galaxy_coords = {}
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == '#':
                image[i][j] = galaxy
                galaxy_coords[galaxy] = (i, j)
                galaxy += 1
    return image, galaxy_coords

def manh_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def galaxy_dists(galaxy_coords, blanks):
    # Galaxy pairs
    galaxy_pairs = list(itertools.combinations(range(len(galaxy_coords)), 2))
    gap = 1e6-1
    tot_dist = 0
    for pair in galaxy_pairs:
        first_galaxy = galaxy_coords[pair[0]]
        second_galaxy = galaxy_coords[pair[1]]
        dist = manh_dist(*first_galaxy, *second_galaxy)
        
        min_row = min(first_galaxy[0], second_galaxy[0])
        max_row = max(first_galaxy[0], second_galaxy[0])
        min_col = min(first_galaxy[1], second_galaxy[1])
        max_col = max(first_galaxy[1], second_galaxy[1])
        for row in range(min_row, max_row):
            if row in blanks['row']:
                dist += gap
        for col in range(min_col, max_col):
            if col in blanks['col']:
                dist += gap
        tot_dist += dist
    return tot_dist
# expanded_image = expand(parse_image(example))
target_expanded = """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#......."""
# for line in expanded_image:
#     print(''.join(line))
# if not np.array_equal(expanded_image, parse_image(target_expanded)):
#     for line in expanded_image:
#         print(''.join(line))
#     print('Not equal')
#     for line in parse_image(target_expanded):
#         print(''.join(line))
# else:
#     print('Equal')

image = parse_image(get_input_file())
# image = parse_image(example)
expansions = expand(image)

expanded_image, galaxy_coords = number_galaxies(image)

print(galaxy_dists(galaxy_coords, expansions))
# Answer 9647174