import numpy as np

def array_to_string(arr):
    return ''.join(arr)

def split_string(s, delimiter):
    return s.split(delimiter)

def reassemble_string(segments, delimiter):
    return delimiter.join(segments)

# Example usage
arr = np.array(['O', '.', 'O', '#', '.', 'O', '.', '#', '#', 'O', '.', '.'])
arr_str = array_to_string(arr)

# Split
split_arr = split_string(arr_str, '#')
print("Split Array:", split_arr)

# Reassemble
reassembled_str = reassemble_string(split_arr, '#')
reassembled_arr = np.array(list(reassembled_str))
print("Reassembled Array:", reassembled_arr)
