# obfuscate_with_cython: True
import numpy as np


def pure_python_function(arr):
    print("I'm a pure Python function!")
    res = 0
    for i in range(len(arr)):
        res += arr[i]
    return res


def numpy_function(arr):
    print("I'm a NumPy function!")
    return np.sum(arr)
