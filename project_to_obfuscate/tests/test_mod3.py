import numpy as np
from some_package.mod3_nb import sum_nb


def test_sum_nb():
    arr = np.arange(10)
    assert sum_nb(arr) == 45
