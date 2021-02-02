"""
Pyx Wrapper to enable the use of cpp function as python function

Due to type conventions, this module should not be used directly, the python module defined should be used instead
Adding underscore will prevent unintentional exports, thus all function defined shoud begin with underscore
"""

import numpy as np
cimport numpy as np

# Import functions from header file
cdef extern from "../cpp/NbrRegionSegment.h":
    cdef void segment(unsigned char *n, int x, int y, int z, int thres, unsigned char *Y)
    cdef int get_regions(unsigned char * n, int x, int y, int z, int thres, unsigned char *ret, int *count)

def _SegmentWrapper(np.ndarray[unsigned char, ndim=3] X, thres):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)

    # Create c type array to store result
    cdef np.ndarray[unsigned char, ndim=3, mode="c"] Y = np.zeros_like(X)
    
    # Call the function
    segment(&X[0,0, 0], X.shape[0], X.shape[1], X.shape[2], thres, &Y[0, 0, 0])

    # Return array
    return Y

def _RegionExtractWrapper(np.ndarray[unsigned char, ndim=3] X, thres):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)

    # Create c type array to store result
    cdef np.ndarray[unsigned char, ndim=2, mode="c"] Y = np.zeros((X.shape[0], X.shape[1]), dtype = X.dtype)
    cdef np.ndarray[int, ndim=1, mode="c"] regions = np.zeros((X.shape[0]*X.shape[1]), dtype= "int32")
    
    # Call the function
    reg = get_regions(&X[0,0, 0], X.shape[0], X.shape[1], X.shape[2], thres, &Y[0, 0], &regions[0])

    # Return array
    return Y, regions[:reg]