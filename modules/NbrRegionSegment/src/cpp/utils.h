#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>
#include <math.h>
#include <set>
#include <algorithm>

#define MAT2D vector<vector<int>>
#define MAT3D vector<vector<vector<int>>>

using namespace std;

float greyscale(vector<int> &pt);

void add(map<int, int> &eqtable, int v1, int v2);

float norm(vector<int> &p1, vector<int> &p2);

bool match(int i1, int j1, int i2, int j2, MAT3D &grid, int thres);

bool matchLbp(int i1, int j1, int i2, int j2, MAT3D &grid, int thres, MAT2D &lbp, float wr, float wg, float wb, float wc);

void bar(int part, int total);

void removeNoise(vector<vector<int>> &lbl);
