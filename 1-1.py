import pandas as pd
import requests

# Read file from https://adventofcode.com/2023/day/1/input
cookie=''
file = 'https://adventofcode.com/2023/day/1/input'
response = requests.get(file, cookies={'session':cookie})
example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
digit_string_dict = {'one':(1, 0), 'two':(2,0), 'three':(3,0), 'four':(4,0), 'five':(5,0), 'six':(6,0),
                     'seven':(7,0), 'eight':(8,0), 'nine':(9,0)}

# Find first and last number in each line of example
val = 0
dataset = response.text
# dataset = example
# dataset = example2
for init_line in dataset.split('\n'):
    first, last = 0, 0
    # Convert digit sstrings to digits
    line = init_line
    if not line.strip():  # Skip empty lines
        continue
    for i in range(len(line)):
        for dig_len in range(3, 6):
            substr = line[i:i+dig_len]
            if substr in digit_string_dict.keys():
                line = line[:i] + str(digit_string_dict[substr][0]) + line[i+1:]
                digit_string_dict[substr] = (digit_string_dict[substr][0], digit_string_dict[substr][1]+1)
                i=0
    for key, value in digit_string_dict.items():
        line = line.replace(key, str(value))
    for char in line:
        if char.isdigit():
            first = char
            break
    for char in line[::-1]:
        if char.isdigit():
            last = char
            break
    val+=int(first+last)
    print(init_line, line, int(first+last), val)
print(digit_string_dict)

print(val)


# ChatGPT's answer
def sum_calibration_values(lines):
    total_sum = 0
    digit_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    for line in lines:
        first_digit = None
        last_digit = None

        # Check for the first digit or digit-word from the start
        for word in digit_words:
            if line.startswith(word):
                first_digit = str(digit_words.index(word) + 1)
                line = line[len(word):]
                break
        if not first_digit:
            for char in line:
                if char.isdigit():
                    first_digit = char
                    break

        # Check for the last digit or digit-word from the end
        for word in digit_words:
            if line.endswith(word):
                last_digit = str(digit_words.index(word) + 1)
                break
        if not last_digit:
            for char in reversed(line):
                if char.isdigit():
                    last_digit = char
                    break

        if first_digit and last_digit:
            calibration_value = int(first_digit + last_digit)
            total_sum += calibration_value

    return total_sum

# Example usage
calibration_data = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen"
]

print(sum_calibration_values(calibration_data))  # Output should be 281
