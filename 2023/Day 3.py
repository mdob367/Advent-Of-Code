import pandas as pd
import requests

def get_input_file():
    # Read session_cookie.txt
    with open('session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2023/day/3/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

def read_schematic(schematic):
    schematic = schematic.split('\n')
    # Add border of '.'
    schematic = ['.'+row+'.' for row in schematic]
    schematic = ['.'*len(schematic[0])] + schematic + ['.'*len(schematic[0])]

    schematic = [list(row) for row in schematic]
    total = 0
    for i, row in enumerate(schematic):
        lin_total = 0

        for num in find_number(row):
            symb_adj = False
            start, end = num[0]
            for j in range(start, end+1):
                if symbol_adjacent(schematic, i, j):
                    symb_adj = True
                    break
            if symb_adj:
                lin_total += num[1]
        total += lin_total
    print(total)
    return schematic

def find_gears(schematic):
    total=0
    schematic = schematic.split('\n')
    # Add border of '.'
    schematic = ['.'+row+'.' for row in schematic]
    schematic = ['.'*len(schematic[0])] + schematic + ['.'*len(schematic[0])]

    schematic = [list(row) for row in schematic]
    asterisks = {}
    for i, row in enumerate(schematic):
        for num in find_number(row):
            found = []
            start, end = num[0]
            for j in range(start, end+1):
                ast = adjacent_asterisk(schematic, i, j)
                if ast and ast not in found:
                    asterisks[ast] = asterisks.get(ast, []) + [num[1]]
                    
                    found.append(ast)


    for key, value in asterisks.items():
        if len(value) == 2:
            # Gear!
            total += value[0]*value[1]

    print('Gear Ratio Total:', total)

def find_number(line):
    numbers = []
    start=None
    for i, char in enumerate(line):
        if char.isdigit():
            if start is not None:
                num += char
            else:
                start=i
                num = char
        elif start is not None:
            numbers.append(((start, i-1), int(num)))
            start=None

    return numbers

def symbol_adjacent(schematic, row, col):
    # Symbols are anything besides digits or '.'
    # try:
    #     # print (schematic[row][col]) and surrounding symbols
    #     print(schematic[row-1][col-1:col+2])
    #     print(schematic[row][col-1:col+2])
    #     print(schematic[row+1][col-1:col+2])
    #     print('\n')

    # except:
    #     pass
    non_symb = '0123456789.'
    if row > 0 and schematic[row-1][col] not in non_symb:
        return True
    if row < len(schematic)-1 and schematic[row+1][col] not in non_symb:
        return True
    if col > 0 and schematic[row][col-1] not in non_symb:
        return True
    if col < len(schematic[0])-1 and schematic[row][col+1] not in non_symb:
        return True
    # Diagonals
    if row > 0 and col > 0 and schematic[row-1][col-1] not in non_symb:
        return True
    if row > 0 and col < len(schematic[0])-1 and schematic[row-1][col+1] not in non_symb:
        return True
    if row < len(schematic)-1 and col > 0 and schematic[row+1][col-1] not in non_symb:
        return True
    if row < len(schematic)-1 and col < len(schematic[0])-1 and schematic[row+1][col+1] not in non_symb:
        return True
    
    return False

def adjacent_asterisk(schematic, row, col):
    ast = '*'
    if row > 0 and schematic[row-1][col] in ast:
        return (row-1, col)
    if row < len(schematic)-1 and schematic[row+1][col] in ast:
        return (row+1, col)
    if col > 0 and schematic[row][col-1] in ast:
        return (row, col-1)
    if col < len(schematic[0])-1 and schematic[row][col+1] in ast:
        return (row, col+1)
    # Diagonals
    if row > 0 and col > 0 and schematic[row-1][col-1] in ast:
        return (row-1, col-1)
    if row > 0 and col < len(schematic[0])-1 and schematic[row-1][col+1] in ast:
        return (row-1, col+1)
    if row < len(schematic)-1 and col > 0 and schematic[row+1][col-1] in ast:
        return (row+1, col-1)
    if row < len(schematic)-1 and col < len(schematic[0])-1 and schematic[row+1][col+1] in ast:
        return (row+1, col+1)
    
    return None

# print(read_schematic(example))
read_schematic(example)
# read_schematic(get_input_file())
find_gears(example)
find_gears(get_input_file())