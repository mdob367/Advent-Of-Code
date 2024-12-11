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

def find_activations(puzz_input):
    activated = ''
    do_pattern = re.compile(r'do\(\)')
    for seq in re.split(do_pattern, puzz_input):
        dont_pattern = re.compile(r"don't\(\)")
        activated += re.split(dont_pattern, seq)[0]
    return activated


def find_mults(puzz_input):
    pattern = re.compile(r'mul\(\d+,\d+\)')
    return re.findall(pattern, puzz_input)

def find_nums(mult):
    pattern = re.compile(r'\d+')
    return re.findall(pattern, mult)


def calc_mult(puzz_input):
    total = 0
    mults = find_mults(puzz_input)
    for mul in mults:
        nums = find_nums(mul)
        total += int(nums[0]) * int(nums[1])
    return total


test_input ="""
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
test_input ="""
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""


# puzz_input = (parse_input(test_input))
# puzz_input = (parse_input(get_input.get_input_file(2)))
# print(puzz_input)

puzz_input = test_input
puzz_input = get_input.get_input_file(3)

# Part 1
# print(calc_mult(puzz_input))

# Part 2
puzz_input = puzz_input
print(calc_mult(find_activations(puzz_input)))