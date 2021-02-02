from .NbrRegionSegment import *
import cv2 as cv
import numpy as np
import time

def SegmentImage(img, thres, show_time = False):
    t = time.time()

    res = SegmentWrapper(img, thres)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res


def SegmentImageByPath(img_path, thres, show_time = False):
    img = cv.imread(img_path)

    t = time.time()

    res = SegmentWrapper(img, thres)
    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res

def RegionExtractImage(img, thres, show_time = False):
    t = time.time()

    res, reg = RegionExtractWrapper(img, thres)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res, reg


def RegionExtractByPath(img_path, thres, show_time = False):
    img = cv.imread(img_path)

    t = time.time()

    res, reg = RegionExtractWrapper(img, thres)
    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res, reg