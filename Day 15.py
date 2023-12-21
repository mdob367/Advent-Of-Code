import numpy as np
import re
import math
import itertools
import requests
from functools import lru_cache
import time
import functools
import cProfile
import pstats
import collections




def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/15/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt


def parse_inp_str(input_str):
    # Remove \n
    input_str = input_str.replace('\n', '')
    input_str = input_str.split(',')
    return input_str

example = """HASH"""
example2 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

def get_ascii(c):
    return ord(c)

def process_char(c, curr_val=0):
    asc = get_ascii(c)
    curr_val += asc
    curr_val *= 17
    curr_val %= 256
    return curr_val

def process_action(action, boxes):
    if '=' in action:
        label, val = action.split('=')
        val = int(val)
        op = '='
    elif '-' in action:
        label = action[:-1]
        op = '-'
    box = get_box(label)
    print(label, box, op)
    if op == '=':
        boxes[box][label] = val
    elif op == '-':
        # Remove if exists
        if label in boxes[box]:
            del boxes[box][label]

    return boxes



def get_box(label):
    curr_val = 0
    for c in label:
        curr_val = process_char(c, curr_val)
    return curr_val


def calc_power(boxes):
    power = 0

    for box, lenses in boxes.items():
        slot = 0
        for val in lenses.values():
            slot+=1
            focus = val * slot
            power += focus * (1+box)
    return power


def process_input(source='ex'):
    
    if source == 'ex':
        input = example
    elif source == 'ex2':
        input = example2
    else:
        input = get_input_file()
    input = parse_inp_str(input)
    
    
    boxes={i: collections.OrderedDict() for i in range(256)}

    for action in input:
        print(action)
        boxes = process_action(action, boxes)
        print(boxes[0], boxes[3])
    
    print(calc_power(boxes))
    exit()
    return boxes

print(process_input(''))

