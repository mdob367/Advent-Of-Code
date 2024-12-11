import numpy as np
import re
import math
import itertools
import get_input


def parse_input(puzz_input = get_input.get_input_file(1)):
    puzz_input = [[int(y) for y in x.split()] for x in puzz_input.split('\n') if x]
    # transpose 
    puzz_input = list(zip(*puzz_input))
    return puzz_input


def count_dist(puzz_input):
    col1 = sorted(list(puzz_input[0]))
    col2 = sorted(list(puzz_input[1]))
    # pairwise distance
    dist = 0
    for i in range(len(col1)):
        dist += abs(col1[i] - col2[i])
    return dist

def calc_score(puzz_input):
    id_vals = set(puzz_input[0])

    score = 0
    for id_v in id_vals:
        score += id_v * puzz_input[0].count(id_v) * puzz_input[1].count(id_v)
    return score

# print(parse_input())
test_input ="""
3   4
4   3
2   5
1   3
3   9
3   3"""
# puzz_input = (parse_input(test_input))
puzz_input = (parse_input())
# print(count_dist(puzz_input))
print(count_dist(puzz_input))
print(calc_score(puzz_input))
