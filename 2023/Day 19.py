import numpy as np
import re
import math
import itertools
import get_input
from functools import lru_cache
from collections import OrderedDict


def parse_map(acc_rej_map):
    rules, parts = acc_rej_map.split('\n\n')
    rule_list = {}
    for rule in rules.split('\n'):
        name, rle = rule.split('{')
        rule_list[name] = OrderedDict()
        rle = rle[:-1]
        rle = rle.split(',')
        prev=[]
        for r in rle:
            r = r.split(':')
            if len(r) == 1:
                rule_list[name][';'.join(prev)] = r[0]
            else:
                rule_list[name][';'.join(prev + [r[0]])] = r[1]
            if '<' in r[0]:
                prev_r = r[0].split('<')
                prev.append(prev_r[0] + '>' + str(int(prev_r[1]) - 1))
            elif '>' in r[0]:
                prev_r = r[0].split('>')
                prev.append(prev_r[0] + '<' + str(int(prev_r[1]) + 1))
    parts = parts.split('\n')
    parts_list = []
    for part in parts:
        part_dict = {}
        for prt in part[1:-1].split(','):
            k, v = prt.split('=')
            part_dict[k] = v
        parts_list.append(part_dict)
    return rule_list, parts_list

example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""



def check_rule(rule, part):
    if rule == 'All Else':
        return True
    else:
        rule = rule.replace(rule[0], part[rule[0]])
        return eval(rule)
    
def apply_rule(rules, part):

    for rule, res in rules.items():
        if check_rule(rule, part):
            if rule[1] == 'A':
                return 'A'
            elif rule[1] == 'R':
                return 'R'
            else:
                return res

def acc_rej(rule_list, part):
    rule = rule_list['in']
    while True:
        rule = apply_rule(rule, part)
        if rule == 'A':
            return sum([int(v) for v in part.values()])
            # return 1
        elif rule == 'R':
            return 0
        else:
            rule = rule_list[rule]

def reduce_rules(rule_list, start='in'):
    if all(v in ['A', 'R'] for v in rule_list[start].values()):
        return rule_list
    else:
        new_rules = OrderedDict()
        prev_rules = []

        for rule, path in rule_list[start].items():
            if path in ['A', 'R']:
                new_rules[';'.join(prev_rules + [rule])] = path
            else:
                for r, p in rule_list[path].items():
                    new_rules[';'.join(prev_rules + [rule] + [r])] = p
            # prev_rules.append(rule.translate(''.maketrans('<>', '><')))
        rule_list[start] = new_rules
        return reduce_rules(rule_list, start)





def accept_sum(rule_list, parts):
    return sum([acc_rej(rule_list, part) for part in parts])

rules, parts = parse_map(get_input.get_input_file(19))
# rules, parts = parse_map(example)

reduced_rules = reduce_rules(rules, 'in')['in']


def count_acc(rules):
    while True:
        print('here it is')
        tot_options = 0
        accept_rules = {}
        reject_rules = {}
        print(*rules.items(), sep='\n')
        orig_range = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
        for i, r in enumerate(rules.items()):
            rule, acc = r
            if acc == 'A' or acc == 'R':
                new_rule_range = {}
                for rl in rule.split(';'):
                    if rl == 'All Else':
                        continue
                    else:
                        xmas = rl[0]
                        curr_range = new_rule_range.get(xmas, orig_range[xmas])
                        if rl[1] == '<':
                            new_rule_range[xmas] = [curr_range[0], min(int(rl.split('<')[1])-1, curr_range[1])]
                        elif rl[1] == '>':
                            new_rule_range[xmas] = [max(int(rl.split('>')[1])+1, curr_range[0]), curr_range[1]]
                for xmas in 'xmas':
                    if xmas not in new_rule_range:
                        new_rule_range[xmas] = orig_range[xmas]
                prod = 1
                for key, vals in new_rule_range.items():
                    prod *= (vals[1] - vals[0] + 1)
                print(rule, new_rule_range, prod)
                if acc == 'A':
                    accept_rules[i] = new_rule_range
                else:
                    reject_rules[i] = new_rule_range

                mult = None
                for key, vals in new_rule_range.items():
                    if mult is None:
                        mult = vals[1] - vals[0] + 1
                    else:
                        mult *= (vals[1] - vals[0] + 1)
                    if mult < 0:
                        break
                if mult is not None:
                    tot_options += mult

        print('\n')
        print('Accepts')
        runnint_tot = 0
        for k, v in accept_rules.items():
            size = 1
            for p in v.values():
                size *= (p[1] - p[0] + 1)
                if size < 0:
                    print('error!')
            print(k, v, size)
            if size > 0:
                runnint_tot += size
        print('Total', runnint_tot)
        print('\n')
        print('Rejects')
        for k, v in reject_rules.items():
            size = 1
            for p in v.values():
                size *= (p[1] - p[0] + 1)
            print(k, v, size)

            runnint_tot += size
        print('Total', runnint_tot)

        return math.pow(4000, 4) - runnint_tot


print(count_acc(reduced_rules))