import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.getcwd()),"modules"))

from NbrRegionSegment import GetAllSegVariance, RegionExtract

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern

img = cv.imread(r"D:\Project 2\Project_2\Region_Growing\2.jpg")


img = cv.resize(img, (0,0), fx = 0.5, fy = 0.5)
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

radius = 1
points = 8*radius 

lbp = local_binary_pattern(gray_img, points, radius, "uniform").astype("uint8")

resa = []
resb = []
sm = []

for i in range(1, 31, 5):
    r1, r2 = RegionExtract(img, lbp, i, 0.4, 0.4, 0.8, True)

    a, b = GetAllSegVariance(gray_img, r1, r2.shape[0], True)
    print(a, b)

    resa.append(a)
    resb.append(b)

    sm.append(a+b)

print(resa, resb)

plt.plot(range(1, 31, 5), resa, label="Intra")
plt.plot(range(1, 31, 5), resb, label="Inter")
plt.plot(range(1, 31, 5), sm, label="Sum")
plt.show()

# r1, r2 = RegionExtract(img, lbp, 20, 0.2, True)
# a, b = GetAllSegVariance(gray_img, r1, r2.shape[0], True)

print(a, b)