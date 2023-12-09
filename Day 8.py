import pandas as pd
import requests
import numpy as np
import re
import math


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

def parse_network(map):
    directions, map = map.split('\n\n')
    map = map.split('\n')
    network = {}
    for line in map:
        node, dest = line.split(' = ')
        left, right = dest[1:-1].split(', ')
        network[node] = (left, right)
    return network, directions

def follow_network(network, directions):
    start_nodes = []
    destination_nodes = []
    for node in network:
        if node[-1]=='A':
            start_nodes.append(node)
        if node[-1]=='Z':
            destination_nodes.append(node)

    current_node = start_node
    next_node = start_node
    steps = 0

    while next_node != destination_node:
        if directions[steps % len(directions)] == 'R':
            side = 1
        else:
            side = 0
        next_node = network[current_node][side]
        current_node = next_node
        steps += 1
    return steps

print(follow_network(*parse_network(get_input_file())))
