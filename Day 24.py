import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time
import sympy


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

    # Actually, time doesn't matter. Forget this.
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

divisors_cache = {}
def timely_iteration(hail_stones):
    for dimen in range(1):
        hail_stones = sorted(hail_stones, key=lambda x: x.pos[dimen])

        low_stone, high_stone = hail_stones[0], hail_stones[-1]
        print(low_stone.pos, high_stone.pos)
        i = 0
        while i< 1000:
            # move by one
            for stone in hail_stones:
                stone.pos[dimen] += stone.vel[dimen]
            hail_stones = sorted(hail_stones, key=lambda x: x.pos[dimen])
            print(hail_stones[0].pos, hail_stones[-1].pos)
            i+=1
    

def find_poss_rock_velo_oned(hail_stones):

    rock_range = [[np.inf, 0], [np.inf, 0], [np.inf, 0]]
    velo_range = [[np.inf, 0], [np.inf, 0], [np.inf, 0]]

    for stone in hail_stones:
        for i, pos in enumerate(stone.pos):
            rock_range[i] = [min(rock_range[i][0], pos), max(rock_range[i][1], pos)] 
            velo_range[i] = [min(velo_range[i][0], stone.vel[i]), max(velo_range[i][1], stone.vel[i])]
    poss_ddt=[]
    for dimen in range(3):
        hail_stones = sorted(hail_stones, key=lambda x: x.vel[dimen])

        test_range = (rock_range[dimen][1] - rock_range[dimen][0]) // 10000000000

        # for rock_pos in range(int(rock_range[dimen][0] - test_range), rock_range[dimen][1] + test_range):
        for start, end, step in [[rock_range[dimen][0],  int(rock_range[dimen][0] - test_range), -1],
                                 [rock_range[dimen][1],  int(rock_range[dimen][1] + test_range), 1]]:
            for rock_pos in range(start, end, step):
                speeds_list = None
                if rock_pos % 10000 == 0:
                    print(rock_pos, len(poss_ddt))
                for hail_stone_i in range(len(hail_stones) // 2 + 1):
                    for stone_i in [hail_stone_i, len(hail_stones)-hail_stone_i-1]:
                        stone = hail_stones[stone_i]
                        pos1 = stone.pos[dimen]
                        vel1 = stone.vel[dimen]

                        # Calculate distances and get divisors using vectorized operations
                        d = np.abs(pos1 - rock_pos)
                        times_list = divisors_cache[d] if d in divisors_cache else sympy.divisors(d)
                        # Calculate speeds using vectorized operations
                        if speeds_list is None:
                            if rock_pos == pos1:
                                continue
                            else:
                                speeds_list = [(pos1 - rock_pos) // t + vel1 for t in times_list]
                        else:
                            next_speeds_list = [(pos1 - rock_pos) // t + vel1 for t in times_list]
                            new_speeds_list = []
                            for spd in next_speeds_list:
                                if spd in speeds_list or rock_pos == pos1 and abs(spd)<1000:
                                    new_speeds_list.append(spd)
                            speeds_list = new_speeds_list
                    if len(speeds_list) == 0 or (max(speeds_list) <= velo_range[dimen][1] and min(speeds_list) >= velo_range[dimen][0]):
                        speeds_list = []
                        break
                if speeds_list:
                    poss_ddt.append((rock_pos, speeds_list))
            print(poss_ddt)
        # Check conditions using vectorized operations
        for i, spd_array in enumerate(speeds_array):
            rock_pos = rock_positions[i]
            for spd in spd_array:
                conditions = np.array([(spd == stone.vel[dimen] and stone.pos[dimen] == rock_pos) or 
                                    (spd != stone.vel[dimen] and (stone.pos[dimen] - rock_pos) % (spd - stone.vel[dimen]) == 0) 
                                    for stone in hail_stones[1:]])
                if np.all(conditions):
                    poss_ddt[dimen].append((rock_pos, spd))
        print(poss_ddt)

    print(*poss_ddt, sep='\n')
def find_poss_rock_velo(rock_pos, hailstone):
    # dy/dx = dy/dt / dx/dty=dy/dt*t+y0		
    # x=dx/dt*t+x0
    # t=(x-x0)/dxdt	
	# y=dydt/dxdt*(x-x0)+y0
	# y=dydx*(x-x0)+y0=dydx*(x-x0)+y0	
	# (dydxA-dydxB)*x-dydxAx0A+dydxBx0B=y0B-y0A
    # x = (y0B-y0A+dydxAx0A-dydxBx0B) / (dydxA-dydxB)


    x1, y1, z1 = hailstone.pos
    x_v1, y_v1, z_v1 = hailstone.vel
    x2, y2, z2 = rock_pos


    if abs(x1 - x2) not in divisors_cache:
        divisors_cache[abs(x1 - x2)] = sympy.divisors(abs(x1 - x2))
    if abs(y1 - y2) not in divisors_cache:
        divisors_cache[abs(y1 - y2)] = sympy.divisors(abs(y1 - y2))
    if abs(z1 - z2) not in divisors_cache:
        divisors_cache[abs(z1 - z2)] = sympy.divisors(abs(z1 - z2))

    # divisors_x = divisors_cache[abs(x1 - x2)]
    # if not divisors_x:
    #     return 'Skip'
    # poss_rocks = []
    # for t in divisors_x:
    #     if t == 1:
    #         continue
    #     dx = (x1 + x_v1 * t - x2) / t
    #     dy = (y1 + y_v1 * t - y2) / t
    #     dz = (z1 + z_v1 * t - z2) / t
    #     if dx.is_integer() and dy.is_integer() and dz.is_integer():
    #         poss_rocks.append((dx, dy, dz))
    # return poss_rocks

    # divisors_x = divisors_cache[abs(x1 - x2)]
    # divisors_y = sympy.divisors(abs(y1 - y2))
    # divisors_z = sympy.divisors(abs(z1 - z2))

    divisors_x = divisors_cache[abs(x1 - x2)]
    divisors_y = divisors_cache[abs(y1 - y2)]
    divisors_z = divisors_cache[abs(z1 - z2)]
    
    # Efficient intersection of sorted divisor lists
    intersection = divisors_x
    if divisors_y:
        intersection = [t for t in intersection if t in divisors_y]
    if divisors_z:
        intersection = [t for t in intersection if t in divisors_z]

    poss_rocks = []
    for t in intersection:
        if t == 1:
            continue
        dx = (x1 + x_v1 * t - x2) / t if divisors_x else x_v1
        dy = (y1 + y_v1 * t - y2) / t if divisors_y else y_v1
        dz = (z1 + z_v1 * t - z2) / t if divisors_z else z_v1
        
        poss_rocks.append((dx, dy, dz))

    return poss_rocks


def rock_collision(rock, hailstone):
    x1, y1, z1 = rock[0]
    dx1, dy1, dz1 = rock[1]

    x2, y2, z2 = hailstone.pos
    dx2, dy2, dz2 = hailstone.vel

    if dx2 == dx1:
        if x1 != x2:
            return False
        if dy2 == dy1:
            if y1 != y2:
                return False
            if dz2 == dz1:
                if z1 != z2:
                    return False
                return True
            t = (z1-z2) / (dz2-dz1)
            if t<0:
                return False
            if abs(x1+dx1*t - (x2+dx2*t))>1e-6 or abs(y1+dy1*t - (y2+dy2*t))>1e-6:
                return False
            return True
        t = (y1-y2) / (dy2-dy1)
        if t<0:
            return False
        if abs(x1+dx1*t - (x2+dx2*t))>1e-6 or abs(z1+dz1*t - (z2+dz2*t))>1e-6:
            return False
        return True

    t = (x1-x2) / (dx2-dx1)

    if t<0 or not t.is_integer():
        return False
    if abs(y1+dy1*t - (y2+dy2*t))>1e-6 or abs(z1+dz1*t - (z2+dz2*t))>1e-6:
        return False
    return True


example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
example2 = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
22, 19, 20 @ -2, -2, -3
24, 25, 28 @ -3, -1, -1
38, 34, 31 @ -5, -2, -1
20, 19, 15 @  1, -5, -3"""
example = example.replace('Hailstone A: ', '').replace('Hailstone B: ', '')

def find_collisions(hail_stones, bounds):
    collisions = []
    for hail_pair in itertools.combinations(hail_stones, 2):
        if intersect(hail_pair, bounds):
            collisions.append(hail_pair)
    return collisions

def find_rock(hail_stones):
    rock_range = [[np.inf, 0], [np.inf, 0], [np.inf, 0]]
    # Arrange hailstones by position
    hail_stones = sorted(hail_stones, key=lambda x: x.pos)
    for stone in hail_stones:
        for i, pos in enumerate(stone.pos):
            rock_range[i] = [min(rock_range[i][0], pos), max(rock_range[i][1], pos)] 

    x_range = (rock_range[0][1] - rock_range[0][0])//1
    y_range = (rock_range[1][1] - rock_range[1][0])//1
    z_range = (rock_range[2][1] - rock_range[2][0])//1
    for x in range(int(rock_range[0][0] - x_range), rock_range[0][1] + x_range):
        
        # print('X is', x)
        for y in range(int(rock_range[1][0] - y_range), rock_range[1][1] + y_range):
            # print('     Y is', y)
            for z in range(int(rock_range[2][0] - z_range), rock_range[2][1] + z_range):
                # if z%100000 == 0:
                    # print('            Z is', z)
                rock_pos = (x, y, z)
                # rock_pos = (24, 13, 10)
                poss_velos = find_poss_rock_velo(rock_pos, hail_stones[0])
                # print('Found Poss Velos', len(poss_velos))
                if poss_velos == 'Skip':
                    continue
                for rock_velo in poss_velos:
                    # print(rock_pos, poss_velos)
                    for stone in hail_stones:
                        if not rock_collision((rock_pos, rock_velo), stone):
                            # print("Missed it")
                            break
                    else:
                        print("Found it!", rock_pos, rock_velo)
                        # exit()


def new_try(hail_list, bypass_ddt=False):
    hail_stones = parse_hail(hail_list)
    def common_divisors(locs):
        distances = [abs(locs[i] - locs[i+1]) for i in range(len(locs)-1)]
        divisors_sets = [set(sympy.divisors(num)) for num in distances if num != 0]
        common_divs = set.intersection(*divisors_sets)
        return common_divs

    if bypass_ddt:
        rock_ddt = bypass_ddt
    else:
        poss_ddt = [None] * 3

        grouped_stones = dict()
        for dimen in range(3):
            ns = dict()
            for stone in hail_stones:
                ns[stone.vel[dimen]] = ns.get(stone.vel[dimen], []) + [stone]
            grouped_stones[dimen] = ns

            # Find potential velocities
            # print(ns)
            for vel, stones in sorted(ns.items(), key=lambda x: len(x[1]), reverse=True):
                # print(locs, poss_ddt[dimen])
                # print(vel, locs, common_divisors(locs))
                locs = [stone.pos[dimen] for stone in stones]
                velos = [d - vel for d in common_divisors(locs)] + [d + vel for d in common_divisors(locs)]
                # print(vel, len(locs), velos)
                velos = [abs(v) for v in velos]
                if poss_ddt[dimen] is None:
                    poss_ddt[dimen] = set(velos)
                else:
                    poss_ddt[dimen] = poss_ddt[dimen].intersection(set(velos))
                if len(poss_ddt[dimen]) ==1:
                    print("Remaining", dimen, poss_ddt[dimen])
                    break
    rock_ddt = [list(poss_ddt[dimen])[0] for dimen in range(3)]
    orig_rock_ddt = rock_ddt.copy()
    ns = grouped_stones[0]
    common_x_vel = sorted(ns.items(), key=lambda x: len(x[1]), reverse=True)[0]
    common_loc = common_x_vel[1]
    print('Common Vel', [(st.pos, st.vel) for st in common_loc])

    common_loc = sorted(common_loc, key=lambda x: x.pos[0])
    dt1 = (common_loc[1].pos[0] - common_loc[0].pos[0]) / (rock_ddt[0] - common_x_vel[0])
    if not dt1.is_integer() or dt1<0:
        rock_ddt[0] = -rock_ddt[0]
        common_loc = sorted(common_loc, key=lambda x: x.pos[0], reverse=True)
        dt1 = (common_loc[1].pos[0] - common_loc[0].pos[0]) / (rock_ddt[0] - common_x_vel[0])

    # common_loc = sorted(common_loc, key=lambda x: x.pos[1])
    # t0 is the time of the first collision, not t=0

    t0 = (dt1 * (rock_ddt[1] - common_loc[1].vel[1]) - (common_loc[1].pos[1] - common_loc[0].pos[1])) / (common_loc[1].vel[1] - common_loc[0].vel[1])
    if not t0.is_integer() or t0<0:
        rock_ddt[1] = -rock_ddt[1]
        t0 = (dt1 * (rock_ddt[1] - common_loc[1].vel[1]) - (common_loc[1].pos[1] - common_loc[0].pos[1])) / (common_loc[1].vel[1] - common_loc[0].vel[1])
    
    t0_z = (dt1 * (rock_ddt[2] - common_loc[1].vel[2]) - (common_loc[1].pos[2] - common_loc[0].pos[2])) / (common_loc[1].vel[2] - common_loc[0].vel[2])
    if t0_z != t0:
        rock_ddt[2] = -rock_ddt[2]
        t0_z = (dt1 * (rock_ddt[1] - common_loc[1].vel[2]) - (common_loc[1].pos[2] - common_loc[0].pos[2])) / (common_loc[1].vel[2] - common_loc[0].vel[2])

    # t0 is the time of the first collision, not t=0
    print('ddt', rock_ddt)
    print('dt1', dt1)
    print('t0  ', t0)
    print('t0_z', t0_z)
    print('First stone', common_loc[0].pos, common_loc[0].vel)
    stone_t0 = [common_loc[0].pos[i] + common_loc[0].vel[i] * t0 for i in range(3)]
    print('Stone at t0', stone_t0)
    rock_init = [stone_t0[i] - rock_ddt[i] * t0 for i in range(3)]
    print('Rock init', rock_init)
    return sum(rock_init)

    

# hail_list = get_input.get_input_file(24)
# print(len(find_collisions(parse_hail(hail_list), [200000000000000, 400000000000000])))
# hail_list = example
# hail_list = example2
# print(len(find_collisions(parse_hail(hail_list), [7, 27])))
# import cProfile
# cProfile.run('find_rock(parse_hail(hail_list))')
# cProfile.run('find_poss_rock_velo_oned(parse_hail(hail_list))')
# timely_iteration(parse_hail(hail_list))
# find_poss_rock_velo_oned(parse_hail(hail_list))
# print(find_rock(parse_hail(hail_list)))
# import cProfile
# new_try(hail_list, [-3, 1, 2])
hail_list = get_input.get_input_file(24)
# cProfile.run('new_try(hail_list)')
print('Answer:', new_try(hail_list))
