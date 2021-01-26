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


import numpy as np
import cv2
from matplotlib import pyplot as plt

# load an image
img = cv2.imread("input.jpg")

cv2.imshow("Disp", img)

# Params for the performing the segmentation.
threshold = 10.0

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
    return (color, oldCol)


def eucl_dist(v1, v2):
    return np.linalg.norm(v1 - v2)


# code to start with the segmentation
p1 = stack.pop()
p2 = stack.pop()

regions = list()
colors = list()

# initially form regions manually
eucl_dist = eucl_dist(p1["Val"], p2["Val"])


if eucl_dist < threshold:
    new_col, colors = gen_color(colors)
    reg = {"pixels": [p1["Coord"], p2["Coord"]], "values": [
        p1["Val"], p2["Val"]], "mean": 0.0, "col": new_col}
    reg["mean"] = np.mean(reg["values"])

    output[p1["Coord"]] = new_col
    output[p2["Coord"]] = new_col

    regions.append(reg)
else:
    new_col, colors = gen_color(colors)
    reg = {"pixels": [p1["Coord"]], "values": [
        p1["Val"]], "mean": 0.0, "col": new_col}
    reg["mean"] = np.mean(reg["values"])

    output[p1["Coord"]] = new_col

    regions.append(reg)

    new_col, colors = gen_color(colors)
    reg = {"pixels": [p2["Coord"]], "values": [
        p2["Val"]], "mean": 0.0, "col": new_col}
    reg["mean"] = np.mean(reg["values"])

    output[p2["Coord"]] = new_col

    regions.append(reg)

# start now with traversing the array of regions and stack
while len(stack) > 0:
    r1 = stack.pop()

    for r in regions:
        dist = eucl_dist(r1["Val"], r["mean"])

        # combine
        if dist < threshold:
            r["pixels"].append(r1["Coord"])
            r["values"].append(r1["Val"])
            r["mean"] = np.mean(r["values"])

            output[r1["Coord"]] = r["col"]
        else:


cv2.waitKey(0)
