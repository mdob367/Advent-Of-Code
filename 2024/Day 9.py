import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy



def parse_input(input):
    input = [int(v) for v in input]

    return input

def compress(puzz_input):
    if len(puzz_input)%2 == 0:
        # Last value is a blank
        puzz_input = puzz_input[:-1]

    blanks = puzz_input[1::2]
    values = puzz_input[::2]
    rev_values = puzz_input[-1::-2]

    compressed = []

    block_id = 0
    rev_block_id = len(puzz_input)//2
    for blank_space in blanks:
        compressed += [block_id] * values[block_id]
        
        while blank_space > 0:

            while rev_values[0] == 0:
                rev_values = rev_values[1:]
                rev_block_id -= 1
                if rev_block_id == block_id:
                    break
            if rev_block_id == block_id:
                break

            compressed.append(rev_block_id)

            blank_space -= 1
            rev_values[0] -= 1
        block_id += 1

        if block_id == rev_block_id:
            while rev_values[0] > 0:
                compressed.append(rev_block_id)
                rev_values[0] -= 1
            break

    return compressed


def block_compress(puzz_input):
    spans = {}
    blanks = []
    end=0
    memory = 0
    for block, count in enumerate(puzz_input):
        start = end
        end = start + count
        memory += count
        if block%2 == 0:
            spans[block//2] = (start, end)
        else:
            blanks.append((start, end))
    blanks = consolidate_blanks(blanks)

    files = sorted(list(spans.keys()), reverse=True)
    for span in files:
        loc = spans[span]
        length = loc[1] - loc[0]
        for i, blank in enumerate(blanks):
            if blank[0] > loc[0]:
                break
            if blank[1] - blank[0] >= length:
                spans[span] = blank[0], blank[0] + length
                blank = (blank[0] + length, blank[1])
                blanks[i] = blank
                break
        blanks = consolidate_blanks(blanks)
    # print(spans.items())
    # print(blanks)

    compressed = [0] * memory
    for span, loc in spans.items():
        for i in range(loc[0], loc[1]):
            compressed[i] = span
    # print(compressed)
    return compressed


def consolidate_blanks(blanks):
    new_blanks = []
    for blank in blanks:
        if new_blanks and new_blanks[-1][1] == blank[0]:
            new_blanks[-1] = (new_blanks[-1][0], blank[1])
        elif blank[0] == blank[1]:
            continue
        else:
            new_blanks.append(blank)
    return new_blanks

def checksum(compressed):
    return sum([compressed[i]*i for i in range(len(compressed))])

def calc_checksum(puzz_input):
    compressed = compress(puzz_input)
    return checksum(compressed)

def calc_block_checksum(puzz_input):
    compressed = block_compress(puzz_input)
    return checksum(compressed)


test_input ="""2333133121414131402"""
# test_input ="""12345"""

real_input = get_input.get_input_file(9)
puzz_input = parse_input(real_input)
print(puzz_input)
print(calc_block_checksum(puzz_input))