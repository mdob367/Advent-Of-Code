import pandas as pd
import requests

cookie='53616c7465645f5f4f216029feea81c3742c80b895fbfa83674bed0207b87b23665371794224ce9ba0689a06d4c3f640bf40eabb0ef900e7b14ee90dfb8bdcf1'
file = 'https://adventofcode.com/2023/day/2/input'
response = requests.get(file, cookies={'session':cookie})
input_file = response.text

example="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

def parse_dataset(dataset):
    dataset = dataset.split('\n')
    games = {}
    for game in dataset:
        if game:
            game_num, game = parse_game(game)
            games[game_num] = game
    return games

def parse_game(game):
    game = game.split(': ')
    game_num = int(game[0].split(' ')[1])
    game = game[1].split('; ')
    parsed = []
    for pull in game:
        pull = [[int(i), c] for i, c in (pl.split(' ') for pl in pull.split(', '))]
        parsed.append(pull)
    return game_num, parsed

bag = {'red':12, 'green':13, 'blue':14}

def valid_games(dataset, bag):
    valid = []
    for game_num, game in dataset.items():
        if valid_game(game, bag):
            valid.append(game_num)
    return valid

def valid_game(game, bag):
    for pull in game:
        for i, c in pull:
            if bag[c] < i:
                return False
    return True

def smallest_bag(game):
    bag={'red': 0, 'blue': 0, 'green': 0}
    for pull in game:
        for i, c in pull:
            bag[c] = max(i, bag[c])
    return bag

def power(game):
    bag = smallest_bag(game)
    product = 1
    for i in bag.values():
        product*=i
    return product

def power_sum(dataset):
    total = 0
    for game in dataset.values():
        total+=power(game)
    return total

print(input_file)
print(sum(valid_games(parse_dataset(input_file), bag)))
print(power_sum(parse_dataset(example)))
print(power_sum(parse_dataset(input_file)))