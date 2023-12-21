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

def process_group(group):
    curr_val = 0
    print
    for c in group:
        curr_val = process_char(c, curr_val)
    return curr_val

def process_input(source='ex'):
    if source == 'ex':
        input = example
    elif source == 'ex2':
        input = example2
    else:
        input = get_input_file()
    input = parse_inp_str(input)
    run_sum = 0
    for grp in input:
        run_sum += process_group(grp)
    return run_sum

print(process_input(''))

