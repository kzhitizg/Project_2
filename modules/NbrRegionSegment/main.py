from NbrRegionSegment import *
import cv2 as cv
import numpy as np
import time

img = cv.imread("D:\Project 2\Project_2\Region_Growing\\3.jpg")

t = time.time()

res = SegmentWrapper(img.astype("int"), 20).astype("uint8")

total = time.time()-t

print("Time to segment = ", total)

cv.imshow("Original", img)

cv.imshow("segmented", res)

cv.waitKey(0)
