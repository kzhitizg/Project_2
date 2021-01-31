#include "NbrRegionSegment.h"

using namespace std;

// To add a region mapping to the table
void add(map<int, int>& eqtable, int v1, int v2) {
    int mn = min(v1, v2);
    int mx = max(v1, v2);
    if ((eqtable).find(mx) != (eqtable).end() && (eqtable)[mx] != mn)
        add(eqtable, mn, (eqtable)[mx]);
    (eqtable)[mx] = mn;
}

// Function to Calculate the euclidean distance between two same size vectors
float norm(vector<int> &p1, vector<int> &p2){
    if (p1.size() != p2.size()){
        throw length_error("Error calculating eculidean distance between unequal size arrays");
    }

    float res = 0;

    for (int i = 0; i < p1.size(); i++)
    {
        res += pow(p1[i]-p2[i], 2);
    }
    return sqrt(res);
}

// Fucntion to check the merging criteria
bool match(int i1, int j1, int i2, int j2, MAT3D &grid, int thres) {
    vector<int> p1 = grid[i1][j1], p2 = grid[i2][j2];
    if (norm(p1, p2) < thres)
        return true;
    return false;
}

// Function to print the bar
void bar(int part, int total){
    int barWidth = 70;
    float progress = ((float)part) / total;

    std::cout << "[";
    int pos = barWidth * progress;
    for (int i = 0; i < barWidth; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] " << part << " / " << total << "\r";
    std::cout.flush();

    progress += 0.16; // for demonstration only
}

// Function to assign label to each region in the image
vector<vector<int>> label(MAT3D &grid, int thres) {
    int r = grid.size();
    int c = grid[0].size();
    vector<vector<int>> lbl(r, vector<int>(c, 0));
    map<int, int> eqtable;
    int newcomp = 1;
    int total = 0;
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            if ((i > 0 && match(i, j, i - 1, j, grid, thres)) && (j > 0 && match(i, j, i, j - 1, grid, thres))) {
                lbl[i][j] = lbl[i][j - 1];
                    if (lbl[i][j - 1] != lbl[i - 1][j]) {
                        add(eqtable, lbl[i - 1][j], lbl[i][j - 1]);
                    }
            }
            else if ((i > 0 && match(i, j, i - 1, j, grid, thres))) {
                lbl[i][j] = lbl[i - 1][j];
            }
            else if ((j > 0 && match(i, j, i, j - 1, grid, thres))) {
                lbl[i][j] = lbl[i][j - 1];
            }
            else {
                lbl[i][j] = newcomp++;
            }

            // Bar disabled due to performance issues
            // total += 1;
            // if (total % 10000 == 0){

            //     bar(total , (r*c));
            // }
        }
    }

    // cout << endl;
    for (auto x : eqtable) {
        int tmp = x.second;
        while (eqtable.find(tmp) != eqtable.end()) {
            tmp = eqtable[tmp];
        }
        eqtable[x.first] = tmp;
    }

    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++) {
                if (eqtable.find(lbl[i][j]) != eqtable.end()) {
                    lbl[i][j] = eqtable[lbl[i][j]];
            }
        }
    }
    return lbl;
}

// Function to be exported. Takes image array as input and returns image with coloured regions
void segment(ARR_TYPE * n, int x, int y, int z, int thres, ARR_TYPE *ret)
{
    MAT3D img(x, vector<vector<int>>(y, vector<int>(z, 0)));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            for (int k = 0; k < z; k++)
            {
                img[i][j][k] = (int) *(n+z*(y*i+j)+k);
            }
        }
        
    }

    vector<vector<int>> lbl = label(img, thres);

    int r = x, c = y;
    set<int> chk;
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++) {
            chk.insert(lbl[i][j]);
        }
    }

    unordered_map<int, vector<int>> colmap;
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++) {
            if (colmap.find(lbl[i][j]) == colmap.end()) {
                colmap[lbl[i][j]] = vector<int>(3, 0);
                colmap[lbl[i][j]][0] = 255 * rand();
                colmap[lbl[i][j]][1] = 255 * rand();
                colmap[lbl[i][j]][2] = 255 * rand();

            }
        }
    }
    vector<int> color;

    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++) {
            
                color = colmap[lbl[i][j]];
                for (int k = 0; k < z; k++)
                {
                    *(ret+z*(y*i+j)+k) = color[k];
                }
        }
    }
}