import numpy as np
import re
import math
import itertools
import get_input


def parse_input(puzz_input = get_input.get_input_file(1)):
    puzz_input = [[int(y) for y in x.split()] for x in puzz_input.split('\n') if x]
    # transpose 
    # puzz_input = list(zip(*puzz_input))
    return puzz_input




def is_safe(level):
    if level[1] < level[0]:
        move = -1
    elif level[1] > level[0]:
        move = 1
    else:
        return 'unsafe', 1
    for i in range(1, len(level)):
        step = level[i] - level[i-1]
        step *= move
        if step > 3 or step < 1:
            return 'unsafe', i
    return 'safe', None

def damp_safe(level):
    safe, i = is_safe(level)
    if safe == 'safe':
        return 'safe'
    else:
        # print(level[:i] + level[i+1:])
        test_level1 = level[:i] + level[i+1:]
        test_level2 = level[:i-1] + level[i:]

        safe, _ = is_safe(test_level1)
        if safe == 'safe':
            return 'safe'
        
        safe, _ = is_safe(test_level2)
        if safe == 'safe':
            return 'safe'
        return 'unsafe'

def count_safe(puzz_input):
    safe = 0
    for level in puzz_input:
        # print(level, is_safe(level))
        safe += is_safe(level)[0] == 'safe'
    return safe

def count_damp_safe(puzz_input):
    safe_ct = 0
    for level in puzz_input:
        # print(level, is_safe(level))
        safe_ct += damp_safe(level) == 'safe'
        if is_safe(level)[0] == 'unsafe' and damp_safe(level) == 'safe':
           print(level, damp_safe(level))
    return safe_ct


# print(parse_input())
test_input ="""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
5 4 1 3 0
0 3 1 4 5
3 3 4 5 6
3 2 4 5 6
6 5 4 4 3
57 60 62 65 63 65 68
1 3 3 4 5
1 4 3 4 5"""

puzz_input = (parse_input(test_input))
puzz_input = (parse_input(get_input.get_input_file(2)))
# print(puzz_input)
print(count_safe(puzz_input))
print(count_damp_safe(puzz_input))