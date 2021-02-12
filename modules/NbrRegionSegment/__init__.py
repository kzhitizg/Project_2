from .NbrRegionSegment import _SegmentWrapper, _RegionExtractWrapper, _GetBGWrapper, _RemoveBG, _GetAllVariance
import time
import numpy as np

def GetWeightedGrey(img, wr, wg, show_time = True):
    t = time.time()

    newim = (img[:, :, 0]*wr + img[:, :, 1]*wg + img[:, :, 2]*(1-wr-wg)).astype("uint8")

    if show_time:
        total = time.time()-t

        print("Time to Calculate = ", total)

    return newim

def GetAllSegVariance(img, lab, nr, show_time = False):
    t = time.time()

    res = _GetAllVariance(img, lab, nr)

    if show_time:
        total = time.time()-t

        print("Time to Calculate = ", total)

    return res

def SegmentImage(img, lbp, thres, wr, wg, wc, show_time=False):
    t = time.time()

    res = _SegmentWrapper(img, lbp, thres, wr, wg, wc)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res


def RegionExtract(img, lbp, thres, wr, wg, wc, show_time=False):
    t = time.time()

    res, reg = _RegionExtractWrapper(img, lbp, thres, wr, wg, wc)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res, reg


def RemoveBG(img, lbp, thres1, thres2, wr, wg, wc, show_time=False):
    t = time.time()

    ret = _RemoveBG(img, lbp, thres1, thres2, wr, wg, wc)

    if show_time:
        total = time.time()-t

        print("Time to Remove BG = ", total)

    return ret


def GetBgMap(label_map, thres, reg_count, show_time=False):
    t = time.time()

    ret = _GetBGWrapper(label_map, thres, reg_count)

    if show_time:
        total = time.time()-t

        print("Time to Get map = ", total)

    return ret
