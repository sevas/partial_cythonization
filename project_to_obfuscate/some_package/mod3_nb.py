# obfuscate_with_cython: True
from numba import njit

@njit
def sum_nb(arr):
    res = 0
    for i in range(arr.shape[0]):
        res += arr[i]
    return res
