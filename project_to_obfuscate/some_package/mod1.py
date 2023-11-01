
from .mod2 import pure_python_function, numpy_function



def compare_functions(arr):
    print("Comparing functions...")
    res1 = pure_python_function(arr)
    res2 = numpy_function(arr)
    return res1, res2

