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
void Segment(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres, float wr, float wg, float wc, ARR_TYPE *ret);
/*  
    n = 3d input image,
    (x,y,z) = size of image, 
    thres =  threshold to combine regions
    ret = 3d array to store output 
*/

void RemoveMap(int *n, int x, int y, int thres, int *count, int regs, bool *ret);
/*
    n = 2d input label map,
    (x, y, z) = size of image, 
    thres =  threshold to remove region,
    count = 1d array to store individual label pixel count,
    regs = number of regions,
    ret = 2d array to store output 
*/

void SegmentAndRemove(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres1, int thres2, float w, ARR_TYPE *ret);
/*
    n = 2d input label map,
    (x, y, z) = size of image, 
    thres =  threshold to remove region,
    count = 1d array to store individual label pixel count,
    regs = number of regions,
    ret = 2d array to store output 
*/

int GetRegions(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres, float w, int *ret, int *count);
/*
    n = 3d input image,
    (x,y,z) = size of image, 
    thres =  threshold to combine regions
    ret = 2d array to store output 
    count = 1d array to store individual label pixel count
*/