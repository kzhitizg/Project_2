from .NbrRegionSegment import _SegmentWrapper, _RegionExtractWrapper, _GetBGWrapper, _RemoveBG
import time

def SegmentImage(img, thres, show_time = False):
    t = time.time()

    res = _SegmentWrapper(img, thres)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res

def RegionExtract(img, thres, show_time = False):
    t = time.time()

    res, reg = _RegionExtractWrapper(img, thres)

    if show_time:
        total = time.time()-t

        print("Time to segment = ", total)

    return res, reg

def RemoveBG(img, thres1, thres2, show_time = False):
    t = time.time()

    ret = _RemoveBG(img, thres1, thres2)

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