


cdef sum_cy(int n):
    cdef int i, s = 0
    for i in range(n):
        s += i
    return s
