from NbrRegionSegment import _RegionExtractWrapper, _SegmentWrapper, _RemoveBG, _GetAllVariance

import cv2 as cv
import numpy as np
from skimage.feature import local_binary_pattern

img = cv.imread("E:/8thSem/BTP_Research/Project_2/Dataset/" +
                "Case_3_A12-37374-17669" + ".jpg")
# img = cv.resize(img, (0,0), fx = 0.5, fy = 0.5)
# img = cv.imread("D:\Project 2\Project_2\Region_Growing\input.jpg")
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

radius = 1
points = 8*radius

lbp = local_binary_pattern(gray_img, points, radius, "uniform").astype("uint8")

for i in range(10, 50, 5):
    r1, r2 = _RegionExtractWrapper(
        img, lbp, i, 5.12561905e-01, 1.17403947e-01, 8.39755087e-01,)

    a, b = _GetAllVariance(gray_img, r1, r2.shape[0])
    print(a, b, a+b)

# res, reg= _RegionExtractWrapper(img, 10)
# res= _SegmentWrapper(img, 10)
# res= _RemoveBG(img, 10, 1000)

# res2 = _RemoveRegionsWrapper(res, 1000, reg)

# img2 = np.array(img)

# img2[res2] = 0

# cv.imshow("Original", img)
# cv.imshow("Segmented", res)
# print(a, b)

# print(reg.shape, np.max(reg))

# cv.waitKey(0)
