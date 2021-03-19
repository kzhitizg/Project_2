import cv2 as cv
import numpy as np

def GetRedBlueCount(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Otsu thresholding

    _, thresh = cv.threshold(gray[gray<200],0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    red = np.sum(thresh==0)
    blue = np.sum(thresh == 255)

    total = thresh.shape[0]

    return red, blue, red/total, blue/total

def GetNames():
    return [
        "RedCount",
        "BlueCount",
        "RedPercentage",
        "BluePercentage"
    ]