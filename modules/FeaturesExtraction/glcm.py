import numpy as np

from skimage.feature import greycomatrix

def WithoutBgNorm(mat):
    mat[0, :]= 0
    mat[:, 0]= 0

    return mat/np.sum(mat)

def glcmMean(mat):
    return (np.sum(np.arange(0, 256)*np.sum(mat, axis = 1)), 
            np.sum(np.arange(0, 256)*np.sum(mat, axis=0)))

def glcmSd(mat, mux, muy):
    return np.sqrt([np.sum(np.square(np.arange(0, 256)-mux)*np.sum(mat, axis = 1)), 
            np.sum(np.square(np.arange(0, 256)-muy)*np.sum(mat, axis=0))])

def zeroSafeLog(mat):
    ret = np.zeros_like(mat)
    ret[mat != 0] = np.log(mat[mat != 0])
    return ret

def probSumDist(mat):
    ret= np.zeros(256*2 -1)

    for i in range(256):
        for j in range(256):
            ret[i+j] += mat[i][j]

    return ret

def probDiffDist(mat):
    ret = np.zeros(256)

    for i in range(256):
        for j in range(256):
            ret[np.abs(i-j)] += mat[i][j]

    return ret

def diffAverage(mat, pdd = None):
    if pdd is None:
        pdd = probDiffDist(mat)
    return np.sum(np.arange(0, 256)*pdd)

def px(mat):
    return np.sum(mat, axis = 1)

def py(mat):
    return np.sum(mat, axis = 0)

def hxy(mat):
    return Entropy(mat)

def hx(mat):
    ret = px(mat)*zeroSafeLog(px(mat))
    return -np.sum(ret)

def hy(mat):
    ret = py(mat)*zeroSafeLog(py(mat))
    return -np.sum(ret)

def hxy1(mat):
    ret = mat*zeroSafeLog(px(mat).reshape(256, 1)*py(mat).reshape(1, 256))
    return -np.sum(ret)

def hxy2(mat):
    pxy = px(mat).reshape(256, 1)*py(mat).reshape(1, 256)
    ret = pxy*zeroSafeLog(pxy)
    return -np.sum(ret)

# ------------ TO BE EXPORTED ----------------
def ASM(mat):
    return np.sum(np.square(mat))

def Entropy(mat):
    ret = mat*zeroSafeLog(mat)
    return -np.sum(ret)

def Contrast(mat):
    j = np.arange(0, 256)*np.ones((256, 1))
    i = j.T
    return np.sum(np.square(i-j)*mat)

def InverseDiffMoment(mat):
    j = np.arange(0, 256)*np.ones((256, 1))
    i = j.T
    return np.sum((1/(1+np.square(i-j)))*mat)

def Correlation(mat):
    mux, muy = glcmMean(mat)
    sdx, sdy = glcmSd(mat, mux, muy)
    j = np.arange(0, 256)*np.ones((256, 1))
    i = j.T
    return np.sum(mat*((i-mux)*(j-muy)/(sdx*sdy)))

def Variance(mat):
    sd = glcmSd(mat, *glcmMean(mat))
    return sd[0]*sd[1]

def SumAverage(mat, psd = None):
    if psd is None:
        psd = probSumDist(mat)
    return np.sum(np.arange(0, 256*2-1)*psd)

def SumEntropy(mat, psd = None):
    if psd is None:
        psd = probSumDist(mat)
    ret = zeroSafeLog(psd)*psd
    return -np.sum(ret)

def SumVariance(mat, psd=None, sumavg = None):
    if psd is None:
        psd = probSumDist(mat)
    if sumavg is None:
        sumavg = SumAverage(mat, psd)
    return np.sum(np.square(np.arange(0, 256*2-1)-sumavg)*psd)

def DiffVariance(mat, pdd=None, diffavg = None):
    if pdd is None:
        pdd = probDiffDist(mat)
    if diffavg is None:
        diffavg = diffAverage(mat, pdd)
    return np.sum(np.square(np.arange(0, 256)-diffavg)*pdd)

def DiffEntropy(mat, pdd=None):
    if pdd is None:
        pdd = probDiffDist(mat)
    ret = zeroSafeLog(pdd)*pdd
    return -np.sum(ret)

def InverseMeasureOfCorrelation1(mat):
    return (hxy(mat) - hxy1(mat))/max(hx(mat), hy(mat))

def InverseMeasureOfCorrelation2(mat):
    return np.sqrt(1-np.exp(-2*(hxy2(mat)-hxy(mat))))

def AllFeatures(mat):
    """Used to calculate 13 features of a single GLCM matrix

    Args:
        mat (2D matrix): GLCM matrix

    Returns:
        vector: 13 features as vector
    """
    res = np.empty(13, dtype = "float32")
    res[0] = ASM(mat)
    res[1] = Contrast(mat)
    res[2] = InverseDiffMoment(mat)
    res[3] = Entropy(mat)
    res[4] = Correlation(mat)
    res[5] = Variance(mat)
    psd = probSumDist(mat)
    res[6] = SumAverage(mat, psd)
    res[7] = SumEntropy(mat, psd)
    res[8] = SumVariance(mat, psd, res[6])
    pdd = probDiffDist(mat)
    res[9] = DiffEntropy(mat, pdd)
    res[10] = DiffVariance(mat, pdd, diffAverage(mat))
    res[11] = InverseMeasureOfCorrelation1(mat)
    res[12] = InverseMeasureOfCorrelation2(mat)

    return res

def AllFeaturesAllMatrix(mat, hasBG = False):
    """Used to calculate all 13 GLCM features for All distances and orientations

    Args:
        mat (4D array): 4D array, output of inbuilt GLCM
    """

    res = np.empty((mat.shape[2]*mat.shape[3], 13), dtype="float32")

    for i in range(mat.shape[2]):
        for j in range(mat.shape[3]):
            if hasBG:    
                res[i*13+j] = AllFeatures(WithoutBgNorm(mat[:, :, i, j]))
            else:
                res[i*13+j] = AllFeatures(mat[:, :, i, j])
        
    return res.flatten()