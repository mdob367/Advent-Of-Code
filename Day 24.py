import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time


class Hail():
    def __init__(self, hail_coords):
        hail_coords = hail_coords.split('@')
        self.pos = [int(h.strip()) for h in hail_coords[0].split(',')]
        self.vel = [int(h.strip()) for h in hail_coords[1].split(',')]


def parse_hail(hail_stones):
    hail_stones = hail_stones.split('\n')
    hail_stones = [Hail(line) for line in hail_stones]
    return hail_stones

def intersect(hail_pair, bounds):
    # Determine if/where 2 lines intersect in 2D

    # Actuall, time doesn't matter. Forget this.
    #x_v1*t + x1 = x_v2*t + x2
    #y_v1*t + y1 = y_v2*t + y2
    #tx = (x2 - x1) / (x_v1 - x_v2)
    #ty = (y2 - y1) / (y_v1 - y_v2)

    # Use this instead:
    # dy/dx = dy/dt / dx/dty=dy/dt*t+y0		
    # x=dx/dt*t+x0
    # t=(x-x0)/dxdt	
	# y=dydt/dxdt*(x-x0)+y0
	# y=dydx*(x-x0)+y0=dydx*(x-x0)+y0	
	# (dydxA-dydxB)*x-dydxAx0A+dydxBx0B=y0B-y0A
    # x = (y0B-y0A+dydxAx0A-dydxBx0B) / (dydxA-dydxB)


    x1, y1 = hail_pair[0].pos[:2]
    x_v1, y_v1 = hail_pair[0].vel[:2]
    x2, y2 = hail_pair[1].pos[:2]
    x_v2, y_v2 = hail_pair[1].vel[:2]

    dydx1 = y_v1 / x_v1
    dydx2 = y_v2 / x_v2

    if dydx1 == dydx2:
        return False

    
    x = (y2 - y1 + dydx1*x1 - dydx2*x2) / (dydx1 - dydx2)
    # x=14.333
    t1 = (x - x1) / x_v1
    t2 = (x - x2) / x_v2
    y = y_v1 * t1 + y1

    if x>=bounds[0] and x<=bounds[1] and y>=bounds[0] and y<=bounds[1]:
        if t1>0 and t2>0:
            return True
    return False

example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
example = example.replace('Hailstone A: ', '').replace('Hailstone B: ', '')

def find_collisions(hail_stones, bounds):
    collisions = []
    for hail_pair in itertools.combinations(hail_stones, 2):
        if intersect(hail_pair, bounds):
            collisions.append(hail_pair)
    return collisions

    

hail_list = get_input.get_input_file(24)
print(len(find_collisions(parse_hail(hail_list), [200000000000000, 400000000000000])))