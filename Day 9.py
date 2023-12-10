import numpy as np
import re
import math
import itertools
import requests

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/9/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

def parse_data(data):
    data = data.split('\n')
    data = [line.split(' ') for line in data]
    data = [[int(num) for num in line] for line in data]
    return data

def get_new(line):
    lines = [line]
    print(lines)
    next_line = line
    while any([nl != 0 for nl in next_line]):
        next_line = np.diff(next_line)
        lines.append(list(next_line))


    lines[-1] = [0] + lines[-1]
    for i in range(len(lines) - 1):
        i_line = len(lines) - i - 2
        lines[i_line] = [-lines[i_line+1][0] + lines[i_line][0]] + lines[i_line]
    print(lines)
    return lines[0][0]

def get_sum(data):
    total = 0
    for line in data:
        total += get_new(line)
    return total

print(get_sum(parse_data(get_input_file())))