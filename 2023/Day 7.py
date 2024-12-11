import pandas as pd
import requests
import numpy as np
import re
import math

ranks ='AKQT98765432J'[::-1]

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/7/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

def parse_hands(data):
    hands = data.split('\n')
    hands = [hand.split(' ') for hand in hands]
    return hands

def get_type(hand):
    # Get rank of hand
    counts = [hand.count(rank) for rank in ranks]
    J_count = hand.count('J')
    # Drop Js
    counts = counts[1:]
    # Apply J to largest count
    largest = max(counts)
    counts[counts.index(largest)] += J_count

    if 5 in counts:
        hand_type = 7
    elif 4 in counts:
        hand_type =  6
    # Check for full house
    elif 3 in counts and 2 in counts:
        hand_type = 5
    elif 3 in counts:
        hand_type = 4
    elif counts.count(2) == 2:
        hand_type = 3
    elif 2 in counts:
        hand_type = 2
    else:
        hand_type = 1
    return hand_type

def get_rank(cards):
    hand_type = get_type(cards)
    # loc of each individual card
    locs = [ranks.find(card) for card in cards]
    #make into int, padding with 0s
    locs = [str(x).zfill(2) for x in locs]
    rank = int(str(hand_type) + ''.join([str(x) for x in locs]))
    return rank



hands = parse_hands(get_input_file())
hands.sort(key=lambda x: get_rank(x[0]))
print(sum([(i+1)*int(h[1]) for i, h in enumerate(hands)]))