import pandas as pd
import requests
import numpy as np
import re
import math

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/6/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """Time:      7  15   30
Distance:  9  40  200"""


def parse_races(data):
    times, distances = data.split('\n')
    # Remove extra spaces
    times = re.sub(' +', ' ', times)
    distances = re.sub(' +', ' ', distances)
    times = times.split(": ")[1].split(' ')
    distances = distances.split(": ")[1].split(' ')
    # Concatenate for part 2
    times = [''.join(times)]
    distances = [''.join(distances)]
    times = [int(x) for x in times]
    distances = [int(x) for x in distances]
    return times, distances

def winning_times(time, distance):
    # quadratic formula
    button_min = int((time - np.sqrt(time**2 - 4 * distance)) / 2)-1
    button_max = int((time + np.sqrt(time**2 - 4 * distance)) / 2)+1
    while button_max * (time - button_max) <= distance:
        button_max -= 1
    while button_min * (time - button_min) <= distance:
        button_min += 1
    return (button_max - button_min + 1)

def winning_strats(example):
    times, distances = parse_races(example)
    wins = [winning_times(time, distance) for time, distance in zip(times, distances)]
    return wins

print(winning_strats(example))
print(winning_strats(get_input_file()))
print(np.product(winning_strats(example)))
print(np.product(winning_strats(get_input_file())))