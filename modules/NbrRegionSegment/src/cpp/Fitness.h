#include <iostream>
#include <fstream>
#include <map>
#include <unordered_map>
#include <vector>
#include <math.h>
#include <set>
#include <algorithm>
#include <numeric>
#include <bitset>
#include <unordered_set>

#define ARR_TYPE unsigned char
#define MAT2D vector<vector<int>>
#define MAT3D vector<vector<vector<int>>>

float IntraSegVariance(ARR_TYPE *img, int *labelled, int x, int y, int numReg);
/*
    img = 2D image
    labelled = 2D labelled image
    (x,y) = Shape of image
    numReg = Total number of regions
*/

float MoranI(ARR_TYPE *img, int *labelled, int x, int y, int numReg);
/*
    img = 2D image
    labelled = 2D labelled image
    (x,y) = Shape of image
    numReg = Total number of regions
*/