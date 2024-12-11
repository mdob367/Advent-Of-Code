import numpy as np
import re
import math
import itertools
import requests

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/10/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """.....
.S-7.
.|.|.
.L-J.
....."""

example2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

example3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

pipes = {"|":((-1,0), (1, 0)),
            "-":((0, -1), (0, 1)),
            "L":((-1, 0), (0, 1)),
            "J":((-1, 0), (0, -1)),
            "7":((1, 0), (0, -1)),
            "F":((1, 0), (0, 1)),
            ".": ((0, 0), (0, 0)),}

def parse_map(map):
    map = map.split('\n')
    map = [list(line) for line in map]
    map = np.array(map)
    return map

def get_start(map):
    start = np.where(map == 'S')
    start = (start[0][0], start[1][0])
    return start

def move(current, direction):
    return (current[0]+direction[0], current[1]+direction[1])

def loop(map):
    start = get_start(map)
    dist = {start: 0}
    next = []

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (abs(i)+abs(j)) != 1:
                continue
            else:
                inc = move(start, (i, j))
                pipe = pipes[map[inc]]
                for dir in pipe:
                    if move(inc, dir) == start:
                        dist[inc] = 1
                        next.append(inc)
    while True:
        to_next = []
        for node in next:
            pipe = pipes[map[node]]
            for dir in pipe:
                new_node = move(node, dir)
                if new_node in dist:
                    continue
                else:
                    dist[new_node] = dist[node] + 1
                    to_next.append(new_node)
        next = to_next.copy()
        if len(next) == 0:
            break
    return dist
    
# map = parse_map(get_input_file())
map = parse_map(get_input_file())
distances = loop(map)

print(max(distances.values()))
map[map == 'S'] = '|'
# Part II
inside=[]
for line in range(len(map)):
    loop_count = {'F': 0, "L": 0, "J": 0, "7": 0, "|": 0}
    for char in range(len(map[line])):
        node = (line, char)
        if node in distances and map[node] != '-':
            loop_count[map[node]] += 1
        elif node not in distances:
            net_crossings = min(loop_count['F'], loop_count['J']) + min(loop_count['7'], loop_count['L']) + loop_count['|']
            if net_crossings % 2 == 1:
                inside.append(node)


# Display ascii map with I for inside
for node in inside:
    map[node] = 'I'
for line in map:
    print(''.join(line))



print(len(inside))

