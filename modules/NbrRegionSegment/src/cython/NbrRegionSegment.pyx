"""
Pyx Wrapper to enable the use of cpp function as python function

Due to type conventions, this module should not be used directly, the python module defined should be used instead
Adding underscore will prevent unintentional exports, thus all function defined shoud begin with underscore
"""

import numpy as np
cimport numpy as np
from libcpp cimport bool

# Import functions from header file
cdef extern from "../cpp/NbrRegionSegment.h":
    cdef void segment(unsigned char *n, int x, int y, int z, int thres, unsigned char *Y)
    cdef int getRegions(unsigned char * n, int x, int y, int z, int thres, int *ret, int *count)
    cdef void removeMap(int * n, int x, int y, int thres, int *count, int regs, bool *ret)
    cdef void segmentAndRemove(unsigned char * n, int x, int y, int z, int thres1, int thres2, unsigned char *ret)

def _GetBGWrapper(np.ndarray[int, ndim=2] X, thres, np.ndarray[int, ndim=1] reg):
    X = np.ascontiguousarray(X)
    reg = np.ascontiguousarray(reg)

    # Create c type array to store result
    cdef np.ndarray[bool, ndim=2, mode="c"] Y = np.zeros((X.shape[0], X.shape[1]), dtype = "bool")
    
    # Call the function
    removeMap(&X[0,0], X.shape[0], X.shape[1], thres, &reg[0], reg.shape[0], &Y[0, 0])

    # Return array
    return Y

def _SegmentWrapper(np.ndarray[unsigned char, ndim=3] X, thres):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)

    # Create c type array to store result
    cdef np.ndarray[unsigned char, ndim=3, mode="c"] Y = np.zeros_like(X)
    
    # Call the function
    segment(&X[0,0, 0], X.shape[0], X.shape[1], X.shape[2], thres, &Y[0, 0, 0])

    # Return array
    return Y

def _RegionExtractWrapper(np.ndarray[unsigned char, ndim=3] X, np.ndarray[unsigned char, ndim=1] lbp, thres):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)
    lbp = np.ascontiguousarray(lbp)

    # Create c type array to store result
    cdef np.ndarray[int, ndim=2, mode="c"] Y = np.zeros((X.shape[0], X.shape[1]), dtype = "int32")
    cdef np.ndarray[int, ndim=1, mode="c"] regions = np.zeros((X.shape[0]*X.shape[1]), dtype= "int32")
    
    # Call the function
    reg = getRegions(&X[0,0, 0], &lbp[0, 0], X.shape[0], X.shape[1], X.shape[2], thres, &Y[0, 0], &regions[0])

    # Return array
    return Y, regions[:reg]

def _RemoveBG(np.ndarray[unsigned char, ndim=3] X, thres1, thres2):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)

    # Create c type array to store result
    cdef np.ndarray[unsigned char, ndim=3, mode="c"] Y = np.zeros_like(X)
    
    # Call the function
    segmentAndRemove(&X[0,0, 0], X.shape[0], X.shape[1], X.shape[2], thres1, thres2, &Y[0, 0, 0])

    # Return array
    return Y