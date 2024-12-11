import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time

def parse_bricks(brick_list):
    bricks = brick_list.split('\n')
    bricks = [[tuple(int(s) for s in st.split(',')), tuple(int(e) for e in end.split(','))] for st, end in [brick.split('~') for brick in bricks]]
    bricks = reorder_bricks(bricks)
    return bricks

example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


def reorder_bricks(bricks):
    brck = []
    for b in bricks:
        x0, x1 = min(b[0][0], b[1][0]), max(b[0][0], b[1][0])
        y0, y1 = min(b[0][1], b[1][1]), max(b[0][1], b[1][1])
        z0, z1 = min(b[0][2], b[1][2]), max(b[0][2], b[1][2])
        brck.append(((x0, y0, z0), (x1, y1, z1)))
    floor = ((min([b[0][0] for b in bricks]), min([b[0][1] for b in bricks]), 0), (max([b[1][0] for b in bricks]), max([b[1][1] for b in bricks]), 0))
    # insert as first brick
    brck.insert(0, floor)
    return brck

bricks = parse_bricks(get_input.get_input_file(22))

def stack_bricks(bricks, dis_check=False):
    # did_fall = False
    falling = True
    sup_bricks = [bricks[0]]
    fall_guys = []
    while falling:
        falling = False
        # order bricks by z-axis
        bricks.sort(key=lambda x: x[0][2])
        for i, br in enumerate(bricks[1:]):
            supported = False
            # if i % 700 == 0:
            #     print(i, br, len(sup_bricks))
            if br in sup_bricks:
                supported = True
                continue
            for below_brick in bricks[:i+1]:
                if supported:
                    break
                if below_brick[1][2] != br[0][2]-1:
                    continue
                for x_brick in range(br[0][0], br[1][0] + 1):
                    if supported:
                        break
                    for y_brick in range(br[0][1], br[1][1] + 1):
                        if supported:
                            break
                        for below_x in range(below_brick[0][0], below_brick[1][0] + 1):
                            if supported:
                                break
                            for below_y in range(below_brick[0][1], below_brick[1][1] + 1):
                                if x_brick == below_x and y_brick == below_y:
                                    supported = True
                                    break
            if not supported:
                falling = True
                # did_fall = True
                # if dis_check:
                #     return bricks, did_fall
                new_brick = ((br[0][0], br[0][1], br[0][2]-1), (br[1][0], br[1][1], br[1][2]-1))
                if br in fall_guys:
                    fall_guys.remove(br)
                fall_guys.append(new_brick)
                bricks[i+1] = new_brick
            else:
                sup_bricks.append(br)

    return bricks, len(fall_guys)

old_bricks = bricks.copy()
fallen_bricks, fallers = stack_bricks(bricks)
falls = 0
# print(old_bricks == fallen_bricks)
# for b, f in zip(old_bricks, fallen_bricks):
#     print(b, f, b==f)
# print('Check Falls')

for b in fallen_bricks[1:]:
    to_dis = fallen_bricks.copy()
    to_dis.remove(b)
    _, fallers = stack_bricks(to_dis, dis_check=True)
    if fallers>0:
        print(b)
        falls += fallers

print(falls)
