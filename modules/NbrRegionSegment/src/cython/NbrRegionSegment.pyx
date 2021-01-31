"""
Pyx Wrapper to enable the use of cpp function as regular python function
"""

import numpy as np
cimport numpy as np

# Import functions from header file
cdef extern from "../cpp/NbrRegionSegment.h":
    cdef void segment(int *n, int x, int y, int z, int thres, int *Y)

def SegmentWrapper(np.ndarray[int, ndim=3] X, thres):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)

    # Create c type array to store result
    cdef np.ndarray[int, ndim=3, mode="c"] Y = np.zeros_like(X)
    
    # Call the function
    segment(&X[0,0, 0], X.shape[0], X.shape[1], X.shape[2], thres, &Y[0, 0, 0])

    # Return array
    return Y