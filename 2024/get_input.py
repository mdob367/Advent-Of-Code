import requests
import time
import functools

# print working directory
import os
print(os.getcwd())
# update working directory to current


def get_input_file(day):
    # Read session_cookie.txt
    with open('/Users/mattdobrin/Desktop/Python Programs/Advent Of Code/2024/session_cookie.txt') as f:
        cookie = f.read()

    file = 'https://adventofcode.com/2024/day/' + str(day) + '/input'
    response = requests.get(file, cookies={'session':cookie})
    # Remove last line if blank
    txt = response.text
    if txt[-1] == '\n':
        txt = txt[:-1]
    return txt


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__!r} executed in {(end_time - start_time):.4f}s")
        # print(f"{(end_time - start_time):.4f}s")
        return result
    return wrapper
