import pandas as pd
import requests
import numpy as np
import re

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/5/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

def parse_dataset(dataset):
    dataset = dataset.split('\n\n')
    seeds = [int(s) for s in dataset[0].split(': ')[1].split(' ')]
    maps = {i: parse_map(map_txt) for i, map_txt in enumerate(dataset[1:])}
    return maps, seeds

def parse_map(map_txt):
    ag_map = []
    for rng in map_txt.split('\n')[1:]:
        out, inp, length = (int(v) for v in rng.split(' '))
        diff = out-inp
        ag_map.append((inp, inp+length, diff))
    return ag_map

def lowest_loc(maps, seeds):
    lowest_loc = np.inf
    for seed in seeds:
        next_ag = seed
        ag_map = 0
        while ag_map in maps:
            next_map = maps[ag_map]

            for next_inp in next_map:
                if next_ag>=next_inp[0] and next_ag<=next_inp[1]:
                    next_ag = next_ag + next_inp[2]
                    break
            ag_map += 1
        lowest_loc = min(lowest_loc, next_ag)
    return lowest_loc

def long_map(maps, seeds):
    seed_range = [[seeds[i], seeds[i]+seeds[i+1]] for i in range(0, len(seeds), 2)]
    ag_range = seed_range
    ag_map = 0
    while ag_map in maps:
        new_ag_range = []
        for i in range(len(ag_range)):
            seed=ag_range[i]
            next_map = maps[ag_map]
            for next_inp in next_map:
                start, end, diff = next_inp
                # Below Range
                if seed[0]<=start and seed[1]<=start:
                    pass
                # Bottom End
                elif seed[0]<=start and seed[1]<=end:
                    new_ag_range.append([start+diff, seed[1]+diff])
                    seed[1] = start-1
                # Within Range
                elif seed[0]>=start and seed[1]<=end:
                    new_ag_range.append([seed[0]+diff, seed[1]+diff])
                    seed=None
                    break
                # Top End
                elif seed[0]>=start and seed[0]<=end and seed[1]>=end:
                    new_ag_range.append([seed[0]+diff, end+diff])
                    seed[0]=end
                # Above Range
                elif seed[0]>=end and seed[1]>=end:
                    pass
            if seed and seed not in new_ag_range:
                new_ag_range.append([seed[0], seed[1]])
        ag_range = new_ag_range
        ag_range.sort(key=lambda x: x[0])
        ag_map += 1
    return new_ag_range


maps, seeds = parse_dataset(example)
maps, seeds = parse_dataset(get_input_file())

print(lowest_loc(maps, seeds))
final_map = long_map(maps, seeds)
# unzip final map
final_map = [m[0] for m in final_map if m[0] >0]
print(min(final_map))



from operator import itemgetter


def solve_day(my_file):
  data = parse_data(my_file)
  print('Part 1: ', part1(data))
  print('Part 2: ', part2(data))


def parse_data(my_file):
    f=my_file
    result = tuple(
        sorted(([int(num) for num in lines.split()]
                for lines in part.split(':')[1].strip().split('\n')),
               key=itemgetter(1)) for part in f.split('\n\n'))
    for trans in result[1:]:
      for item in trans:
        dest, source, step = item
        item[0] = source
        item[1] = source + step
        item[2] = dest - source
    return result


def find_location(seeds, data):
  for trans in data:
    new_seeds = []
    for seed in seeds:
      for start, finish, move in trans:
        if seed[0] < start:
          if seed[1] <= start:
            new_seeds.append(seed)
            seed = 0
            break
          else:
            new_seeds.append([seed[0], start])
            seed[0] = start
        if start <= seed[0] < finish:
          new_seeds.append([seed[0] + move, min(seed[1], finish) + move])
          if seed[1] <= finish:
            seed = 0
            break
          else:
            seed[0] = finish
      if seed:
        new_seeds.append(seed)
    seeds = new_seeds
  return min(seeds)[0]


def part1(data):
  seeds = [[num, num + 1] for num in data[0][0]]
  return find_location(seeds, data[1:])


def part2(data):
  seeds = data[0][0]
  print(seeds)
  seeds = [[seeds[num], seeds[num] + seeds[num + 1]]
           for num in range(0,
                            len(seeds) - 1, 2)]
  return find_location(seeds, data[1:])

solve_day(get_input_file())