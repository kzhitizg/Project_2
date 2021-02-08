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
    cdef void Segment(unsigned char *n, unsigned char *l, int x, int y, int z, int thres, float wr, float wg, float wc, unsigned char *Y)
    cdef int GetRegions(unsigned char *n, unsigned char *l, int x, int y, int z, int thres, float w, int *ret, int *count)
    cdef void RemoveMap(int * n, int x, int y, int thres, int *count, int regs, bool *ret)
    cdef void SegmentAndRemove(unsigned char * n, unsigned char *l, int x, int y, int z, int thres1, int thres2, float w, unsigned char *ret)

def _GetBGWrapper(np.ndarray[int, ndim=2] X, thres, np.ndarray[int, ndim=1] reg):
    X = np.ascontiguousarray(X)
    reg = np.ascontiguousarray(reg)

    # Create c type array to store result
    cdef np.ndarray[bool, ndim=2, mode="c"] Y = np.zeros((X.shape[0], X.shape[1]), dtype = "bool")
    
    # Call the function
    RemoveMap(&X[0,0], X.shape[0], X.shape[1], thres, &reg[0], reg.shape[0], &Y[0, 0])

    # Return array
    return Y

def _SegmentWrapper(np.ndarray[unsigned char, ndim=3] X, np.ndarray[unsigned char, ndim=2] lbp, thres, wr, wg, wc):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)
    lbp = np.ascontiguousarray(lbp)

    # Create c type array to store result
    cdef np.ndarray[unsigned char, ndim=3, mode="c"] Y = np.zeros_like(X)
    
    # Call the function
    Segment(&X[0,0, 0], &lbp[0, 0], X.shape[0], X.shape[1], X.shape[2], thres, wr, wg, wc, &Y[0, 0, 0])

    # Return array
    return Y

def _RegionExtractWrapper(np.ndarray[unsigned char, ndim=3] X, np.ndarray[unsigned char, ndim=2] lbp, thres, w):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)
    lbp = np.ascontiguousarray(lbp)

    # Create c type array to store result
    cdef np.ndarray[int, ndim=2, mode="c"] Y = np.zeros((X.shape[0], X.shape[1]), dtype = "int32")
    cdef np.ndarray[int, ndim=1, mode="c"] regions = np.zeros((X.shape[0]*X.shape[1]), dtype= "int32")
    
    # Call the function
    reg = GetRegions(&X[0,0, 0], &lbp[0, 0], X.shape[0], X.shape[1], X.shape[2], thres, w, &Y[0, 0], &regions[0])

    # Return array
    return Y, regions[:reg]

def _RemoveBG(np.ndarray[unsigned char, ndim=3] X,  np.ndarray[unsigned char, ndim=2] lbp, thres1, thres2, w):
    # Make the array allocation continuous
    X = np.ascontiguousarray(X)
    lbp = np.ascontiguousarray(lbp)

    # Create c type array to store result
    cdef np.ndarray[unsigned char, ndim=3, mode="c"] Y = np.zeros_like(X)
    
    # Call the function
    SegmentAndRemove(&X[0,0, 0], &lbp[0, 0], X.shape[0], X.shape[1], X.shape[2], thres1, thres2, w, &Y[0, 0, 0])

    # Return array
    return Y