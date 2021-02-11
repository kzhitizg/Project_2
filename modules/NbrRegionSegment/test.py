from NbrRegionSegment import _RegionExtractWrapper, _SegmentWrapper, _RemoveBG, _GetAllVariance

import cv2 as cv
import numpy as np
from skimage.feature import local_binary_pattern

img = cv.imread("E:\8thSem\BTP_Research\Project_2\Region_Growing\1.jpg")
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

radius = 1
points = 8*radius

lbp = local_binary_pattern(gray_img, points, radius, "uniform").astype("uint8")
r1, r2 = _RegionExtractWrapper(img, lbp, 20, 0.2)

a, b = _GetAllVariance(gray_img, r1, r2.shape[0])

# res, reg= _RegionExtractWrapper(img, 10)
# res= _SegmentWrapper(img, 10)
# res= _RemoveBG(img, 10, 1000)

# res2 = _RemoveRegionsWrapper(res, 1000, reg)

# img2 = np.array(img)

# img2[res2] = 0

cv.imshow("Original", img)
# cv.imshow("Segmented", res)
print(a, b)

# print(reg.shape, np.max(reg))

cv.waitKey(0)
