from NbrRegionSegment import *

import cv2 as cv
import numpy as np

img = cv.imread(r"D:\Project 2\Project_2\Region_Growing\1.jpg")

res, reg= RegionExtractWrapper(img, 10)

cv.imshow("Original", img)
cv.imshow("Segmented", res)

cv.waitKey(0)