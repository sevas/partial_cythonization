# obfuscate_with_cython: True
import numpy as np
from pathlib import Path


def pure_python_function(arr):
    print("I'm a pure Python function!")
    res = 0
    for i in range(len(arr)):
        res += arr[i]
    return res


def numpy_function(arr):
    print("I'm a NumPy function!")
    return np.sum(arr)


def sample_data():
    txt = (Path(__file__).parent / "data" / "file1.csv").read_text()
    out = []
    for line in txt.splitlines():
        n, s = line.split(",")
        out.append((int(n), s.lstrip().rstrip()))
    return out
