"""
Here, only neighbouring pixels will be able to combine to a new region.

So, First a stack will be created with all neighbouring pixels
Then they will be popped, checking merging criteria

Structure of Stack = (i1, j1, i2, j2, dist)
"""
import array
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap, to_hex, to_rgb
from matplotlib import pyplot as plt
from progress.bar import IncrementalBar

t = time.time()

# load an image
img = cv2.imread("input3.jpg")

thr = 20

nbrs = np.array([
    [0, -1],
    [-1, 0]
    ], "int8")

# -------------------- Classes -----------------------

class Stack:
    def __init__(self, shape, name, dtype= float):
        self.stack = np.empty(shape, dtype)
        self.i = 0
        self.name = name

    def push(self, ele):
        try:
            self.stack[self.i] = ele
        except IndexError:
            raise RuntimeError(f"{self.name} Stack Overflow")
        self.i +=1
    
    def pop(self):
        if self.i == 0:
            raise RuntimeError(f"{self.name} Stack Underflow")
        self.i -= 1
        return self.stack[self.i]

    def isempty(self):
        return self.i==0

    def __len__(self):
        return self.i

# Generator to give neighbours
def get_neighbour(i :int, j:int):
    global img, nbrs

    for n in nbrs:
        if i+n[0] >= 0 and j+n[1]>=0:
            yield i+n[0], j+n[1], img[i+n[0],j+n[1]]

def iterate_image(img, delta_r_start = 0, delta_r_end = 0, delta_c_start = 0, delta_c_end = 0):
    for i in range(delta_r_start, img.shape[0]+delta_r_end):
        for j in range(delta_c_start, img.shape[1]+delta_c_end):
            yield i, j, img[i,j]

def gen_color(oldCol: set):
    r = np.random.rand()*255
    b = np.random.rand()*255
    g = np.random.rand()*255
    color = (r, g, b)

    if color in oldCol:
        return gen_color(oldCol)

    oldCol.add(color)
    return np.array(color, "uint8")


def eucl_dist(v1, v2):
    return np.linalg.norm(np.float64(v1) - v2)

# ----------------------------------- Main ----------------------------------

regions = np.zeros(img.shape[:-1], "uint64")
n_reg = 0

mapping = {}

bar = IncrementalBar('Region Init', max=img.shape[0]*img.shape[1])

for i1, j1, val in iterate_image(img):
    flag = 0
    for i2, j2, _ in get_neighbour(i1, j1):
        if eucl_dist(val, img[i2, j2]) < thr:
            flag = 1
            if regions[(i1, j1)] == 0:
                regions[(i1, j1)] = regions[(i2, j2)]
            else:
                if regions[(i1, j1)] != regions[(i2, j2)]:
                    frm = regions[(i1, j1)]
                    to = regions[(i2, j2)]
                    if frm != to:
                        mapping[max(frm, to)] = min(frm, to)

    if flag == 0:
        n_reg +=1
        regions[(i1, j1)] = n_reg
    bar.next()


# plt.matshow(regions)
# plt.show()

col_arr = []
colors = set()

col_map = []

for c in range(1, n_reg+1):
    if c not in mapping.keys():
        col_map.append(gen_color(colors))
    else:
        val = c
        while val in mapping.keys():
            # print(val)
            val = mapping[val]
        # print(c, mapping[c], val, len(col_map))
        col_map.append(col_map[int(val-1)])

output = np.empty_like(img)

for i, j, val in iterate_image(regions):
    output[i,j, :] = col_map[int(val-1)]

# plt.imshow(output)
# plt.show()

cv2.imwrite("Output_nbr.jpg", output)

# cv2.waitKey(0)
print()
print(time.time() - t)
print(n_reg)
