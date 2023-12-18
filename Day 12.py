import numpy as np
import re
import math
import itertools
import requests
import time
import functools
import cProfile
import pstats
from functools import lru_cache

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # print(f"Function {func.__name__!r} executed in {(end_time - start_time):.4f}s")
        print(f"{(end_time - start_time):.4f}s")
        return result
    return wrapper

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/12/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """???.###. 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

def parse_schematic(schematic):
    # Replace Multiple '.' with single '.'
    schematic = re.sub(r'\.+', '.', schematic)

    schematic = schematic.split('\n')
    schematic = [line.split(' ') for line in schematic]
    schematic = [[line[0], tuple([int(x) for x in line[1].split(',')])] for line in schematic]

    return schematic

@lru_cache(maxsize=None)
def old_count_options(vals, config, pre_calc_len, start_index=0):
    # print(vals, config, pre_calc_len, start_index)
    val_len = pre_calc_len - start_index
    config_sum = sum(config)
    # print('config_sum', config_sum, 'val_len', val_len, 'start_index', start_index, 'vals', vals)
    if config_sum == 0:
        if val_len == 0:
            return 1
        if '#' in vals[start_index:]:
            return 0
        else:
            return 1
    else:
        if val_len <= 0:
            return 0
    if (config_sum + len(config) - 1) > val_len:
        return 0
    
    
    target = config[0]
    if target == 0:
        return old_count_options(vals, config[1:], pre_calc_len, start_index)
    elif target == val_len and target == config_sum:
        if not '.' in vals[start_index:]:
            return 1
        else:
            return 0

    elif vals[start_index] == '?':
        new_vals = '#' + vals[start_index+1:]
        new_pre_calc_len = len(new_vals)
        return old_count_options(new_vals, config, new_pre_calc_len, 0) + old_count_options(vals, config, pre_calc_len, start_index+1) 
    # Doesn't start with a '?'
    else:
        if vals[start_index] == '.':
            return old_count_options(vals, config, pre_calc_len, start_index+1)
        # Starts with a '#'. Check if run of #s matches target
        elif not '.' in vals[start_index:start_index+target]:
            # Run of #s completes the line 
            if val_len == target:
                if config_sum == target:
                    return 1
                else:
                    return 0
            # Insufficient #s to complete the line
            elif val_len < target:
                return 0
            # Run of #s is followed by another '#'- no bueno
            elif vals[start_index + target] == '#':
                return 0
            else:
                return old_count_options(vals, config[1:], pre_calc_len, start_index+target+1)
        else:
            return 0

@lru_cache(maxsize=None)
def count_options(vals_str, config):
    while vals_str[-1] == '.':
        vals_str = vals_str[:-1]
    while vals_str[0] == '.':
        vals_str = vals_str[1:]

    # print(vals_str, config)
    vals = vals_str.split('.', 1)
    if len(vals) == 1:
        # print('len(vals) == 1', vals_str, config, old_count_options(vals_str, config, len(vals_str), 0))
        return old_count_options(vals_str, config, len(vals_str), 0)
    count = 0
    for c_i in range(len(config)+1):
        left_str = vals[0]
        right_str = vals[1]
        # print("Next Loop", c_i, 'left', left_str, config[:c_i], 'right', right_str, config[c_i:], 'count', count)
        # print("  Old Count", old_count_options(left_str, config[:c_i], len(left_str), 0), old_count_options(right_str, config[c_i:], len(right_str), 0))
        left_count = old_count_options(left_str, config[:c_i], len(left_str), 0)
        if left_count != 0:
            right_count = count_options(right_str, config[c_i:])
            count += left_count * right_count
 
    # print('final count', count)
    return count

def get_count_x_rec(vals, config, start_index=0):
    return old_count_options(vals, config, len(vals), start_index=0)

@timeit
def tot_count(schema, version):
    tot = 0
    for i, line in enumerate(schema):
        # Count '?' in line
        # count = line[0].count('?')

        if version == 'old':
            inc_cnt = old_count_options(*line, len(line[0]), 0)
        elif version == 'new':
            inc_cnt = count_options(*line)
        tot += inc_cnt
        if i%1 == 0:
            continue
            print(i, len(schema), inc_cnt)
    return tot


def exp_sch(schema, mult):
    expanded_schem = []
    for line in schema:
        expanded_schem.append(['?'.join([line[0] for _ in range(mult)]), line[1]*mult])
    return expanded_schem

# Create a Profile object
# profiler = cProfile.Profile()
# profiler.enable()



# profiler.disable()
# stats = pstats.Stats(profiler).sort_stats('cumulative')
# stats.print_stats()

schema = parse_schematic(get_input_file())
# schema = parse_schematic(example)

for mult in [1, 2, 3, 4, 5]:
    expanded_schem = exp_sch(schema, mult)
    print('New Way', mult, tot_count(expanded_schem, 'new'), '\n')
    print('Old Way', mult, tot_count(expanded_schem, 'old'))



# schm = ['???.?', [1, 1]]
# print(count_options(*schm), old_count_options(*schm, len(schm[0]), 0))
# exit()

