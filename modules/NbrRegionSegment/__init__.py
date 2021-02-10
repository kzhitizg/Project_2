from .NbrRegionSegment import _SegmentWrapper, _RegionExtractWrapper, _GetBGWrapper, _RemoveBG, _GetAllVariance
import time

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


def RegionExtract(img, lbp, thres, w, show_time=False):
    t = time.time()

    res, reg = _RegionExtractWrapper(img, lbp, thres, w)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res, reg


def RemoveBG(img, lbp, thres1, thres2, w, show_time=False):
    t = time.time()

    ret = _RemoveBG(img, lbp, thres1, thres2, w)

    if show_time:
        total = time.time()-t

        print("Time to Remove BG = ", total)

    return ret


def GetBgMap(label_map, thres, reg_count, show_time=False):
    t = time.time()

    ret, mp = _GetBGWrapper(label_map, thres, reg_count)

    if show_time:
        total = time.time()-t

        print("Time to Get map = ", total)

    return ret, mp
