import numpy as np
import re
import math
import itertools
import get_input
from copy import deepcopy



def parse_input(input):
    input = [int(v) for v in input]

    return input

def compress(puzz_input):
    if len(puzz_input)%2 == 0:
        # Last value is a blank
        puzz_input = puzz_input[:-1]

    blanks = puzz_input[1::2]
    values = 