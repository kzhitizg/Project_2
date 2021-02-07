#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>
#include <math.h>
#include <set>
#include <algorithm>

#define ARR_TYPE unsigned char
#define MAT2D vector<vector<int>>
#define MAT3D vector<vector<vector<int>>>

// These Function will be exported

void segment(ARR_TYPE *n, int x, int y, int z, int thres, ARR_TYPE *ret);
/*  
    n = 3d input image,
    (x,y,z) = size of image, 
    thres =  threshold to combine regions
    ret = 3d array to store output 
*/

void removeMap(int *n, int x, int y, int thres, int *count, int regs, bool *ret);
/*
    n = 2d input label map,
    (x, y, z) = size of image, 
    thres =  threshold to remove region,
    count = 1d array to store individual label pixel count,
    regs = number of regions,
    ret = 2d array to store output 
*/

void segmentAndRemove(ARR_TYPE *n, int x, int y, int z, int thres1, int thres2, ARR_TYPE *ret);
/*
    n = 2d input label map,
    (x, y, z) = size of image, 
    thres =  threshold to remove region,
    count = 1d array to store individual label pixel count,
    regs = number of regions,
    ret = 2d array to store output 
*/

int getRegions(ARR_TYPE *n, int x, int y, int z, int thres, int *ret, int *count);
/*
    n = 3d input image,
    (x,y,z) = size of image, 
    thres =  threshold to combine regions
    ret = 2d array to store output 
    count = 1d array to store individual label pixel count
*/