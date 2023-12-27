import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict
import time

def parse_config(schema):
    schema = schema.split('\n')
    res = {}
    conj_list = []
    for line in schema:
        module, children = line.split(' -> ')
        if module[0] == '%':
            res[module[1:]] = flipflop(module[1:], children)
        elif module[0] == '&':
            res[module[1:]] = conjuntion(module[1:], children)
            conj_list.append(module[1:])
        elif module == 'broadcaster':
            res[module] = broadcast(module, children)

    for line in schema:
        module, children = line.split(' -> ')
        if module != 'broadcaster':
            module = module[1:]
        for c in children.split(', '):
            if c in conj_list:
                res[c].add_input(module)
    return res


class flipflop():
    def __init__(self, name, children):
        self.name = name
        self.state = 0
        self.children = children.split(', ')

    def hp(self, input):
        return []

    def lp(self, input):
        self.state = 1 - self.state
        if self.state == 1:
            return [(self.name, c, 'high') for c in self.children]
        else:
            return [(self.name, c, 'low') for c in self.children]
        
class conjuntion():
    def __init__(self, name, children):
        self.name = name
        self.children = children.split(', ')
        self.inputs = {}

    def add_input(self, input):
        if input in self.inputs:
            pass
        else:
            self.inputs[input] = 'low'

    def hp(self, input):
        self.inputs[input] = 'high'
        return self.send_pulse()

    def lp(self, input):
        self.inputs[input] = 'low'
        return self.send_pulse()

    def send_pulse(self):
        if all([v == 'high' for v in self.inputs.values()]):
            return [(self.name, c, 'low') for c in self.children]
        else:
            return [(self.name, c, 'high') for c in self.children]
        
class broadcast():
    def __init__(self, name, children):
        self.name = name
        self.children = children.split(', ')
    
    def hp(self, input):
        return [(self.name, c, 'high') for c in self.children]
    
    def lp(self, input):
        return [(self.name, c, 'low') for c in self.children]


example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

example2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

def run_config(config):
    config = parse_config(config)
    pulse_count = {'low': 0, 'high': 0}
    bp=0
    start_time = time.time()
    vr_inputs = {}
    while True:
        stack = [('button', 'broadcaster', 'low')]
        bp+=1
        if bp % 1000000 == 0:
            print(bp, f'({(time.time() - start_time):.0f}s)')
        while stack:
            curr = stack.pop(0)
            if curr[1] == 'rx' and curr[2] == 'low':
                print(bp)
                exit()
            if curr[1] == 'vr' and curr[2] == 'high':
                bp_l = vr_inputs.get(curr[0], [])
                if bp_l == []:
                    vr_inputs[curr[0]] = [bp]
                else:
                    for b in bp_l:
                        if bp%b == 0:
                            break
                    else:
                        vr_inputs[curr[0]] = bp_l + [bp]

                print(curr[0], vr_inputs)
            pulse_count[curr[2]] += 1
            if curr[1] not in config:
                continue
            if curr[2] == 'low':
                stack += config[curr[1]].lp(curr[0])
            else:
                stack += config[curr[1]].hp(curr[0])
    print(pulse_count)


run_config(get_input.get_input_file(20))