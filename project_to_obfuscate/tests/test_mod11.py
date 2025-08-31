from some_package.subpkg import mod11
import numpy as np


def test_numpy_func():
    mod11.another_numpy_function(np.array([1, 2, 3]))
