#include <iostream>
#include <bits/stdc++.h>

#define ARR_TYPE unsigned char
#define MAT2D vector<vector<int>>
#define MAT3D vector<vector<vector<int>>>

// This Function will be exported
void segment(ARR_TYPE * n, int x, int y, int z, int thres, ARR_TYPE *ret);
void bar(int part, int total);
int get_regions(ARR_TYPE * n, int x, int y, int z, int thres, ARR_TYPE *ret, int *count);