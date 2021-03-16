import numpy as np

from skimage.feature import greycomatrix

def WithoutBgNorm(mat):
    mat[0, :]= 0
    mat[:, 0]= 0

    return mat/np.sum(mat)

def _glcmMean(mat):
    return (np.sum(np.arange(0, 256)*np.sum(mat, axis = 1)), 
            np.sum(np.arange(0, 256)*np.sum(mat, axis=0)))

def _glcmSd(mat, mux, muy):
    return np.sqrt([np.sum(np.square(np.arange(0, 256)-mux)*np.sum(mat, axis = 1)), 
            np.sum(np.square(np.arange(0, 256)-muy)*np.sum(mat, axis=0))])

def _zeroSafeLog(mat):
    ret = np.zeros_like(mat)
    ret[mat != 0] = np.log(mat[mat != 0])
    return ret

def _probSumDist(mat):
    ret= np.zeros(256*2 -1)

    for i in range(256):
        for j in range(256):
            ret[i+j] += mat[i][j]

    return ret

def _probDiffDist(mat):
    ret = np.zeros(256)

    for i in range(256):
        for j in range(256):
            ret[np.abs(i-j)] += mat[i][j]

    return ret

def _diffAverage(mat, pdd = None):
    if pdd is None:
        pdd = _probDiffDist(mat)
    return np.sum(np.arange(0, 256)*pdd)

def _px(mat):
    return np.sum(mat, axis = 1)

def _py(mat):
    return np.sum(mat, axis = 0)

def _hxy(mat):
    return Entropy(mat)

def _hx(mat):
    ret = _px(mat)*_zeroSafeLog(_px(mat))
    return -np.sum(ret)

def _hy(mat):
    ret = _py(mat)*_zeroSafeLog(_py(mat))
    return -np.sum(ret)

def _hxy1(mat):
    ret = mat*_zeroSafeLog(_px(mat).reshape(256, 1)*_py(mat).reshape(1, 256))
    return -np.sum(ret)

def _hxy2(mat):
    _pxy = _px(mat).reshape(256, 1)*_py(mat).reshape(1, 256)
    ret = _pxy*_zeroSafeLog(_pxy)
    return -np.sum(ret)

# ------------ TO BE EXPORTED ----------------
def ASM(mat):
    return np.sum(np.square(mat))

def Entropy(mat):
    ret = mat*_zeroSafeLog(mat)
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
    mux, muy = _glcmMean(mat)
    sdx, sdy = _glcmSd(mat, mux, muy)
    j = np.arange(0, 256)*np.ones((256, 1))
    i = j.T
    return np.sum(mat*((i-mux)*(j-muy)/(sdx*sdy)))

def Variance(mat):
    sd = _glcmSd(mat, *_glcmMean(mat))
    return sd[0]*sd[1]

def SumAverage(mat, psd = None):
    if psd is None:
        psd = _probSumDist(mat)
    return np.sum(np.arange(0, 256*2-1)*psd)

def SumEntropy(mat, psd = None):
    if psd is None:
        psd = _probSumDist(mat)
    ret = _zeroSafeLog(psd)*psd
    return -np.sum(ret)

def SumVariance(mat, psd=None, sumavg = None):
    if psd is None:
        psd = _probSumDist(mat)
    if sumavg is None:
        sumavg = SumAverage(mat, psd)
    return np.sum(np.square(np.arange(0, 256*2-1)-sumavg)*psd)

def DiffVariance(mat, pdd=None, diffavg = None):
    if pdd is None:
        pdd = _probDiffDist(mat)
    if diffavg is None:
        diffavg = _diffAverage(mat, pdd)
    return np.sum(np.square(np.arange(0, 256)-diffavg)*pdd)

def DiffEntropy(mat, pdd=None):
    if pdd is None:
        pdd = _probDiffDist(mat)
    ret = _zeroSafeLog(pdd)*pdd
    return -np.sum(ret)

def InverseMeasureOfCorrelation1(mat):
    return (_hxy(mat) - _hxy1(mat))/max(_hx(mat), _hy(mat))

def InverseMeasureOfCorrelation2(mat):
    return np.sqrt(1-np.exp(-2*(_hxy2(mat)-_hxy(mat))))

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
    psd = _probSumDist(mat)
    res[6] = SumAverage(mat, psd)
    res[7] = SumEntropy(mat, psd)
    res[8] = SumVariance(mat, psd, res[6])
    pdd = _probDiffDist(mat)
    res[9] = DiffEntropy(mat, pdd)
    res[10] = DiffVariance(mat, pdd, _diffAverage(mat))
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