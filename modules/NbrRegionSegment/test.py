from NbrRegionSegment import _RegionExtractWrapper, _SegmentWrapper, _RemoveBG

import cv2 as cv
import numpy as np

img = cv.imread(r"D:\Project 2\Project_2\Region_Growing\1.jpg")

# res, reg= _RegionExtractWrapper(img, 10)
# res= _SegmentWrapper(img, 10)
# res= _RemoveBG(img, 10, 1000)

# res2 = _RemoveRegionsWrapper(res, 1000, reg)

# img2 = np.array(img)

# img2[res2] = 0

cv.imshow("Original", img)
cv.imshow("Segmented", res)

# print(reg.shape, np.max(reg))

cv.waitKey(0)