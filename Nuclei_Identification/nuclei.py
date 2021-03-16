#!/usr/bin/env python
# coding: utf-8

# In[141]:


import sys
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from skimage.feature import local_binary_pattern


# In[142]:


sys.path.append(os.path.join(os.path.dirname(os.getcwd()),"modules"))


# In[143]:


import NbrRegionSegment as seg


# In[144]:

def run(path):

    img = cv.imread(path)


    # In[145]:


    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


    # In[146]:


    #LBP part
    radius = 3
    points = 8*radius 

    lbp = local_binary_pattern(gray_img, points, radius, "uniform").astype("uint8")


    wr, wb, wg, wc = 0.87433346,  0.99435252,  0.,          0.9
    thres = 12
    r = seg.RemoveBG(img, lbp, thres, 1000, wr, wg, wb, wc)


    # In[153]:


    # plt.imshow(r)


    # In[154]:


    # plt.imshow(seg.SegmentImage(img, lbp, thres, wr, wg, wb, wc))


    # In[155]:


    lmap, reg = seg.RegionExtract(img, lbp, thres, wr, wg, wb, wc)


    # In[156]:


    r_map = seg.GetBgMap(lmap, 1000, reg)


    # In[157]:


    r_white = np.array(img)
    r_white[r_map] = 255


    # In[158]:


    gray = cv.cvtColor(r_white, cv.COLOR_BGR2GRAY)


    plt.imshow(r_white)


    # In[162]:


    ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    # In[164]:


    r_white = np.array(img)
    r_white[r_map] = 255

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thresh,cv.MORPH_CLOSE,kernel, iterations = 2)

    # sure background area
    sure_bg = cv.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
    ret, sure_fg = cv.threshold(dist_transform,0.2*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)

    # # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    markers = cv.watershed(r_white,markers)
    # r_white[markers == -1] = [0, 255,0]

    # In[169]:


    nuc_mask = np.zeros_like(markers) == 0
    nuc_mask[markers == -1] = False

    # In[171]:


    nuc_mask[gray>100] = 0
    nuc_mask[gray<10] = 0


    # In[172]:


    tmp = np.array(r_white, "uint8")

    tmp[nuc_mask] = [0, 255, 0]


    # In[173]:


    tmp2 = np.zeros_like(r_white, "uint8")

    tmp2[nuc_mask] = r_white[nuc_mask]

    # segmented, reg = seg.RegionExtract(tmp2, np.zeros_like(lbp), 20, wr, wg, wb, 1)
    # noise = seg.GetBgMap(segmented, 20, reg)

    # tmp2[~noise] = 0


    # In[174]:


    # tmp2[gray>100] = 0


    # In[176]:


    cv.imshow("img", tmp2)
    cv.imshow("out", img)
    cv.imshow("img2", tmp)
    cv.waitKey(0)


    # In[ ]:




