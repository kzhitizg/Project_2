import numpy as np

# function to return the first moment i.e. mean


def firstmoment(px):
    return np.sum(px)/len(px)

# function to find 2nd moment


def secondmoment(px, mn):
    return np.sqrt(np.sum((px - mn)**2)/len(px))

# func for 3rd moment


def thirdmoment(px, mn):
    return np.float_power(np.sum((px - mn)**3)/len(px), 1/3)

# func for 4th moment


def fourthmoment(px, mn):
    return np.float_power(np.sum((px - mn)**4)/len(px), 1/4)

# function to return the array of 12 features (4 for each channel)


def ColorMoments(img):
    feat = np.empty(12, dtype="float32")

    # get a array of pixels that are not zero or black in color i.e. bg
    non_black_pixels = img[np.any(img != [0, 0, 0], axis=-1)]

    # the features would be in order of B, G, R
    for i in range(0, 3):

        feat[4*i] = firstmoment(non_black_pixels[:, i])  # mean
        mn = feat[4*i]
        feat[4*i + 1] = secondmoment(non_black_pixels[:, i], mn)
        feat[4*i + 2] = thirdmoment(non_black_pixels[:, i], mn)  # skewness
        feat[4*i + 3] = fourthmoment(non_black_pixels[:, i], mn)  # kurtosis

    return feat
