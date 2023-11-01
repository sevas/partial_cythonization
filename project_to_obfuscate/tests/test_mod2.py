from some_package import mod2
import numpy as np


def test_numpy_func():
    mod2.numpy_function(np.array([1, 2, 3]))


def test_pure_py_func():
    mod2.pure_python_function([1, 2, 3])
