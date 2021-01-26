import numpy as np
cimport numpy as np

DTYPE = np.int

ctypedef np.int_t DTYPE_t

def copier(np.ndarray img):
    # copy the array

    cdef np.ndarray ret = np.zeros_like(img)

    cdef int i, j

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            ret[i][j] = img[i][j]

    return ret