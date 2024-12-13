import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy



def parse_input(input):
    puzz_dict = {}
    puzz_dict = {int(i): puzz_dict.get(int(i), 0) + 1 for i in input.split()}
    return puzz_dict


def rules(stone):
    if stone == 0:
        return [1]
    # even number of digits
    elif int(1+math.log10(stone)) % 2 == 0:
        # split left and right sides
        left = int(str(stone)[:len(str(stone))//2])
        right = int(str(stone)[len(str(stone))//2:])
        return [left, right]
    else:
        return [stone*2024]
    

def apply_rules(puzz_input):
    new_puzz = {}
    for stone in puzz_input:
        new_stones = rules(stone)
        for new_stone in new_stones:
            new_puzz[new_stone] = new_puzz.get(new_stone, 0) + puzz_input[stone]

    return new_puzz


def pre_calc():
    res_dict = {}
    for i in range(100):
        stones = {i: 1}
        for steps in range(1, 25):
            stones = apply_rules(stones)
            res_dict[(i, steps)] = stones
    return res_dict


def calc(puzz_input, calc_dict, steps):
    stones = puzz_input
    new_stones = {}
    for step in range(steps):
        missing_stones = {}
        for stone in stones:
            if (stone, steps-step) in calc_dict:
                final = calc_dict[(stone, steps-step)]
                for fin_stone in final:
                    new_stones[fin_stone] = new_stones.get(fin_stone, 0) + final[fin_stone]
            else:
                missing_stones[stone] = missing_stones.get(stone, 0) + stones[stone]
        stones = apply_rules(missing_stones)
    for stone in stones:
        new_stones[stone] = new_stones.get(stone, 0) + stones[stone]
    return new_stones


def tot_stones(stones):
    return sum(stones.values())

test_input ="""125 17"""
# test_input ="""12345"""

real_input = get_input.get_input_file(11)
puzz_input = parse_input(real_input)

calc_dict = {}
print('calced')
stones = calc(puzz_input, calc_dict, 75)
print(stones)

print(75, tot_stones(stones))