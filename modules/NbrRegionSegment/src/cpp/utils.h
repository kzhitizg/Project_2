#include "NbrRegionSegment.h"

using namespace std;

void add(map<int, int> &eqtable, int v1, int v2);

float norm(vector<int> &p1, vector<int> &p2);

bool match(int i1, int j1, int i2, int j2, MAT3D &grid, int thres);

float score(vector<int> p1, vector<int> p2, float wr, float wg);

bool matchLbp(int i1, int j1, int i2, int j2, MAT3D &grid, int thres, MAT2D &lbp, float wr, float wg, float wc);

void bar(int part, int total);

void removeNoise(vector<vector<int>> &lbl);
