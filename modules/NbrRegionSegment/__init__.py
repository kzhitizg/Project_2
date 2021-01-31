from .NbrRegionSegment import *
import cv2 as cv
import numpy as np
import time

def SegmentImage(img, thres, show_time = False):
    t = time.time()

    res = SegmentWrapper(img.astype("int"), thres).astype("uint8")

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res


def SegmentImageByPath(img_path, thres, show_time = False):
    img = cv.imread(img_path)

    t = time.time()

    res = SegmentWrapper(img.astype("int"), thres).astype("uint8")
    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res