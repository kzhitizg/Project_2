import sys
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from skimage.feature import greycomatrix


def SegmentNuclei(img):
    """Function to extract nuclei in image

    Args:
        img (3D ndarray): Input Image

    Returns:
        2d ndarray: Binary image with nuclei as black
    """
    #Convert BG to white, as dark region is ROI
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img[gray == 0] = [255, 255, 255]
    gray[gray == 0] = 255
    r_white = img

    # Otsu thresholding
    _, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    # noise removal, close filled regions
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(thresh,cv.MORPH_CLOSE,kernel, iterations = 2)

    # sure background area
    sure_bg = cv.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
    _, sure_fg = cv.threshold(dist_transform,0.3*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg,sure_fg)

    # Marker labelling
    _, markers = cv.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv.watershed(r_white,markers)

    # create map for image with black as nuclei
    outline = np.zeros_like(markers, "uint8")
    outline[markers == -1] = 255
    outline[thresh == 255] = 255

    # Thresholding to seperate close nuclei regions
    th = np.mean(gray[outline == 0])*0.75
    outline[gray>th] = 255
    outline[gray<10] = 255

    # Noise Removal
    outline = cv.medianBlur(outline, 5)

    # Thresholding again
    outline[gray>th] = 255

    return outline

def GetFeatures(img):
    nuc_mask = SegmentNuclei(img)
    if np.sum(nuc_mask == 0) == 0:
        return np.array([0, 0, 0, 0, 0])

    # Count boundary pixels
    glcm = greycomatrix(nuc_mask, [1], [0, 90], 256)
    P = glcm[0, -1, 0, 0] + glcm[0, -1, 0, 1]

    Area = np.sum(nuc_mask == 0)

    Circularity = 4*np.math.pi*Area/(P**2)

    r, _ = cv.connectedComponents(255-nuc_mask)

    col = np.mean(img[nuc_mask==0])

    return np.array([P, Area, Circularity, r, col])

def GetFeatNames():
    return [
        "Perimeter",
        "Area",
        "Circularity",
        "NucleiCount",
        "MeanColor"
        ]