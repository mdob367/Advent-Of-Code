import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy



def parse_input(input):
    input = input.split('\n')
    input = [row.split(': ') for row in input]
    input = [(int(row[0]), list(map(int, row[1].split()))) for row in input]

    return input

def add_op(target, values, pos=-1):
    if pos == 0:
        return target, [values[0]+values[1]] + values[2:]
    elif pos == -1:
        return target-values[-1], values[:-1]

def mult_op(target, values, pos=-1):
    if pos == 0:
        return target, [values[0] * values[1]] + values[2:]
    elif pos == -1:
        return target//values[-1], values[:-1]

def concat_op(target, values, pos=-1):
    if pos == 0:
        return target, [int(str(values[0]) + str(values[1]))] + values[2:]
    elif pos == -1:
        return target, values[:-2] + [int(str(values[-2]) + str(values[-1]))]

def calculable(target, values):
    if abs(target-int(target)) > 1e-10:
        return False
    if len(values) == 1:
        return target == values[0]
    elif any([val > target for val in values]):
        return False
    
    
    return calculable(*add_op(target, values, pos=0)) or calculable(*mult_op(target, values, pos=0)) or calculable(*concat_op(target, values, pos=0)) 
    

    
def sum_calculable(puzz_input):
    counter = 0
    sum = 0
    for target, values in puzz_input:
        counter += 1
        if calculable(target, values):
            print(target, 'is calculable', counter, 'of', len(puzz_input))
            sum += target
    return sum

test_input ="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

real_input = get_input.get_input_file(7)
puzz_input = parse_input(real_input)
print(sum_calculable(puzz_input))