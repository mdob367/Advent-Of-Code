import pandas as pd
import requests
import numpy as np
import re
import math
import itertools


def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/8/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

example2="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

example3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

def parse_network(map):
    directions, map = map.split('\n\n')
    map = map.split('\n')
    network = {}
    for line in map:
        node, dest = line.split(' = ')
        left, right = dest[1:-1].split(', ')
        network[node] = {'L': left, 'R': right}
    return network, directions

def follow_network(network, directions):
    start_nodes = []
    destination_nodes = []
    for node in network:
        if node[-1]=='A':
            start_nodes.append(node)
        if node[-1]=='Z':
            destination_nodes.append(node)
    print(start_nodes, destination_nodes)

    current_nodes = start_nodes
    next_nodes = start_nodes
    steps = 0
    results = {node:[] for node in start_nodes}

    while any([nn not in destination_nodes for nn in next_nodes]):
        side = directions[steps % len(directions)]
        next_nodes = [network[current_node][side] for current_node in current_nodes]
        current_nodes = next_nodes
        steps += 1
        for i in range(len(next_nodes)):
            nn = next_nodes[i]
            sn = start_nodes[i]
            if nn in destination_nodes:
                if not any([steps % st for st in results[sn]]):
                    results[sn] = results[sn] + [steps]
        if steps % 1000000==0:
            min = np.inf
            for combos in list(itertools.product(*[results[sn] for sn in start_nodes])):                
                new_combo = np.lcm.reduce(combos)
                if new_combo < min:
                    min = new_combo
                    print(min)
    return steps

print(follow_network(*parse_network(get_input_file())))
