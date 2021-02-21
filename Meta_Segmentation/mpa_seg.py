import sys
import pandas as pd
import cv2 as cv
import numpy as np
from tqdm import tqdm
from skimage.feature import local_binary_pattern
import os
import multiprocessing as mp

import time

sys.path.append(os.path.join(os.path.dirname(os.getcwd()),"modules"))


import NbrRegionSegment as seg
from MarinePredator.MPA import MPA


# In[17]:


def get_fit_oneimg(name, wr, wg, wc, thres, res):
    #read the image
    img = cv.imread("../Dataset/" + name + ".jpg")

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #LBP part
    radius = 1
    points = 8*radius 

    lbp = local_binary_pattern(gray_img, points, radius, "uniform").astype("uint8")

    #segment image
    r = seg.RegionExtract(img, lbp, thres, wr, wg, wc)
    r1, r2 = r

    #find the fitness level
    intra, inter = seg.GetAllSegVariance(gray_img, r1, r2.shape[0])

    res.put(intra+inter)


# In[18]:


#fitness function to be used in the marine predator algo
def fitness_func(wr, wg, wc, thres):
    #read the csv file
    data = pd.read_csv("../CSV/reduced.csv")

    #fitness for each image against each predator
    # ctx = mp.set_start_method("forkserver")
    fit = mp.Queue()

    p = [mp.Process(target = get_fit_oneimg, args=(entry[2], wr, wg, wc, thres, fit)) for entry in data.values]

    for proc in p:
        proc.start()

    for proc in p:
        proc.join()

    # #fetch the image file
    # for entry in tqdm(data.values, desc = "Fitness Calculation"):
    #     #push the fitness into the list
    #     get_fit_oneimg(entry[2], wr, wg, wc, thres, fit) #-> fitness is the sum of the inter and intra variance and is a decreasing function
    
    #return the fitness as the avg of all fitness
    arr = [fit.get() for i in range(len(data.values))]
    print(arr)
    return np.mean(arr)

#%%
if __name__ == "__main__":
    t = time.time()
    fitness_func(0.60761819,  0.36488088,  0.22582778, 10.87146632)
    print(time.time()-t)


# In[19]:


# #algo params for the MPA
# max_iter = 30
# num_agents = 15

# #wr, wg, wc, thres
# lb = [0, 0, 0, 10]
# ub = [0.99999999, 0.999999999, 0.99999999, 50]
# num_var = 4

# #create a class object for the metaheuristic algorithm
# mpa = MPA(num_agents, max_iter, lb, ub, num_var, fitness_func)


# # In[20]:


# mpa.initialize()


# # In[21]:


# mpa.Prey.shape


# # In[22]:


# mpa.Prey


# # In[23]:


# # for i in tqdm(mpa.iter_gen(), total = mpa.maxItr):
# #     pass


# # In[ ]:




