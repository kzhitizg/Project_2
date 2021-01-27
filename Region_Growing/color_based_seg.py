'''
Structure of Regions:
The region is a dictionary object with the following values:
- pixels -> list which stores the coordinates of various pixels for each region
- pixel values -> list which stores the pixel values for each region
- mean color -> a representative of the entire region, used to calculate the similarity of a pixel from the region.
- unique color assigned to region

Structure of Elements in Stack:
The tuples in the stack will have the pixel coordinates and the pixel value.
'''
import time

import numpy as np
import cv2
from matplotlib import pyplot as plt
from progress.bar import IncrementalBar

t = time.time()
# load an image
img = cv2.imread("1.jpg")
img = cv2.resize(img, (0, 0), fx = 0.1, fy = 0.1)

print(img.shape)

# cv2.imshow("Disp", img)

# Params for the performing the segmentation.
threshold = 20.0

# numpy array to store the final image
output = np.zeros(img.shape)

# perform the following operations on the entire image
stack = []  # for storing the info of all pixels

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        obj = {"Coord": [i, j], "Val": img[i, j]}
        stack.append(obj)


def gen_color(oldCol: list):
    r = np.random.rand()*255
    b = np.random.rand()*255
    g = np.random.rand()*255
    color = [r, g, b]

    while color in oldCol:
        r = np.random.rand()*255
        b = np.random.rand()*255
        g = np.random.rand()*255
        color = [r, g, b]

    oldCol.append(color)
    return color


def eucl_dist(v1, v2):
    return np.linalg.norm(v1 - v2)


# code to start with the segmentation
p1 = stack.pop()
p2 = stack.pop()

regions = list()
colors = list()

# initially form regions manually
dist = eucl_dist(p1["Val"], p2["Val"])


if dist < threshold:
    new_col = gen_color(colors)
    reg = {"pixels": [p1["Coord"], p2["Coord"]], "values": [
        p1["Val"], p2["Val"]], "mean": 0.0, "col": new_col}
    reg["mean"] = np.mean(reg["values"], axis=0)

    output[p1["Coord"][0], p1["Coord"][1]] = new_col
    output[p2["Coord"][0], p2["Coord"][1]] = new_col

    regions.append(reg)
else:
    new_col = gen_color(colors)
    reg = {"pixels": [p1["Coord"]], "values": [
        p1["Val"]], "mean": 0.0, "col": new_col}
    reg["mean"] = np.mean(reg["values"], axis=0)

    output[p1["Coord"][0], p1["Coord"][1]] = new_col

    regions.append(reg)

    new_col = gen_color(colors)
    reg = {"pixels": [p2["Coord"]], "values": [
        p2["Val"]], "mean": 0.0, "col": new_col}
    reg["mean"] = np.mean(reg["values"])

    output[p2["Coord"][0], p2["Coord"][1]] = new_col

    regions.append(reg)

# start now with traversing the array of regions and stack
bar = IncrementalBar('Countdown', max=len(stack))
for r1 in reversed(stack):
    # r1 = stack.pop()

    flag = False  # to tell if the region can be combined

    for r in regions:
        dist = eucl_dist(r1["Val"], r["mean"])

        # combine
        if dist < threshold:
            r["pixels"].append(r1["Coord"])
            r["values"].append(r1["Val"])
            r["mean"] = np.mean(r["values"], axis=0)

            output[r1["Coord"][0], r1["Coord"][1]] = r["col"]

            flag = True
            break  # move onto the next pixel in stack

    if not flag:
        new_col = gen_color(colors)
        reg = {"pixels": [r1["Coord"]], "values": [
            r1["Val"]], "mean": 0.0, "col": new_col}
        reg["mean"] = np.mean(reg["values"], axis=0)

        output[r1["Coord"][0], r1["Coord"][1]] = new_col

        regions.append(reg)
    # print(len(regions))
    bar.next()
    # time.sleep(1)

cv2.imwrite("Seg.jpg", output)
print(t-time.time())
print(len(regions))

cv2.waitKey(0)
