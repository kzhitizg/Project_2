import example
import cv2 as cv
import numpy as np
import time

img = cv.imread("D:\Project 2\Data_Osteo_Tiles\Data_Osteo_Tiles\Training_Set_1\set1\Case 3 A10-17206-19249.jpg", cv.IMREAD_GRAYSCALE)

def copier(img):
    ret = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]-1):
            ret[i][j] = img[i][j]

    return ret

#cython
t = time.time()
example.copier(img)
print(time.time()-t)

#python
t = time.time()
copier(img)
print(time.time()-t)