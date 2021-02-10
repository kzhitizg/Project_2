import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.getcwd()),"modules"))


from NbrRegionSegment import GetAllSegVariance, RegionExtract

import cv2 as cv
import numpy as np
from skimage.feature import local_binary_pattern

img = cv.imread(r"D:\Project 2\Project_2\Region_Growing\1.jpg")
img = cv.resize(img, (0,0), fx = 0.5, fy = 0.5)
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

radius = 1
points = 8*radius 

lbp = local_binary_pattern(gray_img, points, radius, "uniform").astype("uint8")
r1, r2 = RegionExtract(img, lbp, 20, 0.2, True)

a, b = GetAllSegVariance(gray_img, r1, r2.shape[0], True)

# res, reg= _RegionExtractWrapper(img, 10)
# res= _SegmentWrapper(img, 10)
# res= _RemoveBG(img, 10, 1000)

# res2 = _RemoveRegionsWrapper(res, 1000, reg)

# img2 = np.array(img)

# img2[res2] = 0

# cv.imshow("Original", img)
# cv.imshow("Segmented", res)
print(a, b)

# print(reg.shape, np.max(reg))

cv.waitKey(0)