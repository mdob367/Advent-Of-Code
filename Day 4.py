import pandas as pd
import requests
import math

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/4/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

def parse_cards(cards):
    total = 0
    cards = cards.split('\n')
    card_count = [1 for _ in range(len(cards))]
    for i, card in enumerate(cards):
        card = card.split(': ')[1]
        num = i + 1
        cnt = card_count[num-1]
        winners, mine = card.split(' | ')
        winners = winners.split(' ')
        mine = mine.split(' ')

        matches = 0
        for m in mine:
            if m and m in winners:
                matches += 1
                card_count[num-1+matches] += cnt

    print(sum(card_count))

parse_cards(example)
parse_cards(get_input_file())