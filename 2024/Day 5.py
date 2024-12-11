import numpy as np
import re
import math
import itertools
import get_input


def parse_input(input):
    rules, pages = input.split('\n\n')
    rules = [rule.split('|') for rule in rules.split('\n')]
    rule_dict = {}
    for rl in rules:
        rule_dict[rl[0]] = rule_dict.get(rl[0], set()) | set([rl[1]])
    pages = [page.split(',') for page in pages.split('\n')]
    return rule_dict, pages

def add_dependencies(rules):
    extended_rules = rules.copy()
    for key, rule in rules.items():
        for r in rule:
            if r in rules:
                extended_rules[key] | set(rules[r])
    return extended_rules

def check_rules(pages, rules):
    while pages:
        page = pages.pop()
        if page in rules:
            if any([pg in rules[page] for pg in pages]):
                return False            
    return True

def fix_rules(pages, rules):
    for pg_i in range(len(pages)-1, -1, -1):
        page = pages[pg_i]
        if page in rules:
            for rl in rules[page]:
                if rl in pages[:pg_i]:
                    # swap rl with the element pg_i
                    pages[pg_i], pages[pages.index(rl)] = pages[pages.index(rl)], pages[pg_i]
                    return fix_rules(pages, rules)
    return True, pages

def count_middles(page_set, rules):
    count = 0
    for pages in page_set:
        if check_rules(pages.copy(), rules):
            count += int(pages[len(pages)//2])
    return count

def count_middles_with_fix(page_set, rules):
    count = 0
    for pages in page_set:
        new_pages = fix_rules(pages.copy(), rules)[1]
        count += int(new_pages[len(new_pages)//2])
    return count

test_input ="""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

# rules, pages = (parse_input(test_input))
rules, pages = (parse_input(get_input.get_input_file(5)))
rules = add_dependencies(rules)
already_correct = count_middles(pages, rules)
print(already_correct) # Part 1
print(count_middles_with_fix(pages, rules)-already_correct) # Part 2

exit()
