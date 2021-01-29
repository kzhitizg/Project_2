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
import array
import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from progress.bar import IncrementalBar


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


def reg_growing(img_path):
    t = time.time()
    # load an image
    img = cv2.imread(img_path)
    # img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
    
    def to_2D(pt):
        return pt//img.shape[1], pt%img.shape[1]

    print(img.shape)

    # cv2.imshow("Disp", img)

    # Params for the performing the segmentation.
    threshold = 10.0

    # numpy array to store the final image
    output = np.zeros(img.shape)

    # # perform the following operations on the entire image
    # stack = []  # for storing the info of all pixels

    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):
    #         obj = {"Coord": [i, j], "Val": img[i, j]}
    #         stack.append(obj)

    stack = np.flip(np.reshape(img, (-1, 3)))

    # code to start with the segmentation
    p1 = stack[0]
    p2 = stack[1]

    r_mean = np.zeros_like(stack, "float32")
    r_it = 0
    r_colors = np.zeros_like(stack)
    r_count = array.array('i')
    colors = set()

    # initially form regions manually
    dist = eucl_dist(p1, p2)

    if dist < threshold:
        new_col = gen_color(colors)
        # reg = {"pixels": [to_2D(0), to_2D(1)], "values": [
        #     p1, p2], "mean": 0.0, "col": new_col}
        # reg["mean"] = np.mean(reg["values"], axis=0)

        mean = np.mean([p1, p2], axis=0)

        output[to_2D(0)] = new_col
        output[to_2D(1)] = new_col

        # regions.append(reg)
        r_count.append(2)
        r_mean[r_it] = mean
        r_colors[r_it] = new_col
        r_it += 1

    else:
        new_col = gen_color(colors)
        # reg = {"pixels": [to_2D(0)], "values": [
        #     p1], "mean": 0.0, "col": new_col}
        # reg["mean"] = np.mean(reg["values"], axis=0)

        output[to_2D(0)] = new_col

        # regions.append(reg)

        r_count.append(1)
        r_mean[r_it] = p1
        r_it += 1

        new_col = gen_color(colors)
        # reg = {"pixels": [to_2D(1)], "values": [
        #     p2], "mean": 0.0, "col": new_col}
        # reg["mean"] = np.mean(reg["values"])

        output[to_2D(1)] = new_col

        r_count.append(1)
        r_mean[r_it] = p2
        r_it += 1

    # t = time.time()
    # start now with traversing the array of regions and stack
    bar = IncrementalBar('Countdown', max=stack.shape[0]//100)
    for i in range(2, stack.shape[0]):
        r1 = stack[i]
        # r1 = stack.pop()

        flag = False  # to tell if the region can be combined

        for j in range(len(r_count)):
            dist = eucl_dist(r1, r_mean[j])

            # combine
            if dist < threshold:
                # r["pixels"].append(to_2D(i))
                # r["values"].append(r1)
                # r["mean"] = np.mean(r["values"], axis=0)

                r_mean[j] = (r_mean[j]*r_count[j] + r1)/(r_count[j]+1)
                # print(r_mean)
                # exit(0)
                r_count[j] += 1

                output[to_2D(i)] = r_colors[j]

                flag = True
                break  # move onto the next pixel in stack

        if not flag:
            new_col = gen_color(colors)
            # reg = {"pixels": [to_2D(i)], "values": [
            #     r1], "mean": 0.0, "col": new_col}
            # reg["mean"] = np.mean(reg["values"], axis=0)

            output[to_2D(i)] = new_col

            # regions.append(reg)
            r_count.append(1)
            r_mean[r_it] = r1
            r_colors[r_it] = new_col
            r_it += 1
        # print(len(regions))

        if i%100 == 0:
            bar.next()

        # time.sleep(1)

    cv2.imwrite("10Seg"+img_path, output)
    print()
    print(r_it)

    # plt.matshow(output)
    # # cv2.waitKey(0)
    # plt.show()

    print(t-time.time())
    print(len(colors))

if __name__ == "__main__":
    reg_growing("1.jpg")
    reg_growing("2.jpg")
    reg_growing("3.jpg")