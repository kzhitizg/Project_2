#include "NbrRegionSegment.h"
#include "utils.h"
// #include <bits/stdc++.h>

using namespace std;

// Function to assign label to each region in the image
vector<vector<int>> label(MAT3D &grid, int thres)
{
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
            if ((i > 0 && match(i, j, i - 1, j, grid, thres)) && (j > 0 && match(i, j, i, j - 1, grid, thres)))
            {
                lbl[i][j] = lbl[i][j - 1];
                if (lbl[i][j - 1] != lbl[i - 1][j])
                {
                    add(eqtable, lbl[i - 1][j], lbl[i][j - 1]);
                }
            }
            else if ((i > 0 && match(i, j, i - 1, j, grid, thres)))
            {
                lbl[i][j] = lbl[i - 1][j];
            }
            else if ((j > 0 && match(i, j, i, j - 1, grid, thres)))
            {
                lbl[i][j] = lbl[i][j - 1];
            }
            else
            {
                lbl[i][j] = newcomp++;
            }

            // Bar disabled due to performance issues
            // total += 1;
            // if (total % 10000 == 0){

            //     bar(total , (r*c));
            // }
        }
    }

    cout << endl;
    for (auto x : eqtable)
    {
        int tmp = x.second;
        while (eqtable.find(tmp) != eqtable.end())
        {
            tmp = eqtable[tmp];
        }
        eqtable[x.first] = tmp;
    }

    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            if (eqtable.find(lbl[i][j]) != eqtable.end())
            {
                lbl[i][j] = eqtable[lbl[i][j]];
            }
        }
    }
    removeNoise(lbl);

    return lbl;
}

// Function to assign label to each region in the image
vector<vector<int>> labelv2(MAT3D &grid, int thres, MAT2D &lbp, float wr = 0.4, float wg = 0.2, float wb = 0.4, float wc = 0.7)
{
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
            if ((i > 0 && matchLbp(i, j, i - 1, j, grid, thres, lbp, wr, wg, wb, wc)) && (j > 0 && matchLbp(i, j, i, j - 1, grid, thres, lbp, wr, wg, wb, wc)))
            {
                lbl[i][j] = lbl[i][j - 1];
                if (lbl[i][j - 1] != lbl[i - 1][j])
                {
                    add(eqtable, lbl[i - 1][j], lbl[i][j - 1]);
                }
            }
            else if ((i > 0 && matchLbp(i, j, i - 1, j, grid, thres, lbp, wr, wg, wb, wc)))
            {
                lbl[i][j] = lbl[i - 1][j];
            }
            else if ((j > 0 && matchLbp(i, j, i, j - 1, grid, thres, lbp, wr, wg, wb, wc)))

            {
                lbl[i][j] = lbl[i][j - 1];
            }
            else
            {
                lbl[i][j] = newcomp++;
            }

            // Bar disabled due to performance issues
            // total += 1;
            // if (total % 10000 == 0){

            //     bar(total , (r*c));
            // }
        }
    }

    cout << endl;
    for (auto x : eqtable)
    {
        int tmp = x.second;
        while (eqtable.find(tmp) != eqtable.end())
        {
            tmp = eqtable[tmp];
        }
        eqtable[x.first] = tmp;
    }

    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            if (eqtable.find(lbl[i][j]) != eqtable.end())
            {
                lbl[i][j] = eqtable[lbl[i][j]];
            }
        }
    }
    removeNoise(lbl);

    return lbl;
}

// Function to be exported. Takes image array as input and returns image with coloured regions
void Segment(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres, float wr, float wg, float wb, float wc, ARR_TYPE *ret)
{
    MAT3D img(x, vector<vector<int>>(y, vector<int>(z, 0)));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            for (int k = 0; k < z; k++)
            {
                img[i][j][k] = (int)*(n + z * (y * i + j) + k);
            }
        }
    }

    MAT2D lbp(x, vector<int>(y, 0));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            lbp[i][j] = (int)*(n + (y * i + j));
        }
    }

    vector<vector<int>> lbl = labelv2(img, thres, lbp, wr, wg, wb, wc);

    int r = x, c = y;

    unordered_map<int, vector<int>> colmap;
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            if (colmap.find(lbl[i][j]) == colmap.end())
            {
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
        for (int j = 0; j < c; j++)
        {

            color = colmap[lbl[i][j]];
            for (int k = 0; k < z; k++)
            {
                *(ret + z * (y * i + j) + k) = (ARR_TYPE)color[k];
            }
        }
    }
}

int GetRegions(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres, float wr, float wg, float wb, float wc, int *ret, int *count)
{
    MAT3D img(x, vector<vector<int>>(y, vector<int>(z, 0)));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            for (int k = 0; k < z; k++)
            {
                img[i][j][k] = (int)*(n + z * (y * i + j) + k);
            }
        }
    }

    MAT2D lbp(x, vector<int>(y, 0));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            lbp[i][j] = (int)*(n + (y * i + j));
        }
    }

    vector<vector<int>> lbl = labelv2(img, thres, lbp, wr, wg, wb, wc);

    int r = x, c = y;

    unordered_map<int, int> lblmap;
    int till_now = 0;
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            if (lblmap.find(lbl[i][j]) == lblmap.end())
            {
                lblmap[lbl[i][j]] = till_now++;
            }
        }
    }

    for (int i = 0; i < till_now; i++)
    {
        *(count + i) = 0;
    }

    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            *(ret + (y * i + j)) = lblmap[lbl[i][j]];
            *(count + lblmap[lbl[i][j]]) += 1;
        }
    }
    return till_now;
}

void RemoveMap(int *n, int x, int y, int thres, int *count, int regs, bool *ret)
{
    set<int> to_remove;
    for (int i = 0; i < regs; i++)
    {
        if (*(count + i) >= thres)
        {
            to_remove.insert(i);
        }
    }

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            if (to_remove.find(*(n + (y * i + j))) != to_remove.end())
            {
                *(ret + (y * i + j)) = true;
            }
            else
            {
                *(ret + (y * i + j)) = false;
            }
        }
    }
}

void SegmentAndRemove(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres1, int thres2, float wr, float wg, float wb, float wc, ARR_TYPE *ret)
{
    MAT3D img(x, vector<vector<int>>(y, vector<int>(z, 0)));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            for (int k = 0; k < z; k++)
            {
                img[i][j][k] = (int)*(n + z * (y * i + j) + k);
            }
        }
    }
    MAT2D lbp(x, vector<int>(y, 0));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            lbp[i][j] = (int)*(n + (y * i + j));
        }
    }

    vector<vector<int>> lbl = labelv2(img, thres1, lbp, wr, wg, wb, wc);

    int r = x, c = y;

    unordered_map<int, int> lblcount;
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            lblcount[lbl[i][j]]++;
        }
    }

    set<int> to_remove;
    for (auto &&i : lblcount)
    {
        if (i.second >= thres2)
        {
            to_remove.insert(i.first);
        }
    }
    bool remove;
    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            if (to_remove.find(lbl[i][j]) != to_remove.end())
            {
                remove = true;
            }
            else
            {
                remove = false;
            }
            for (int k = 0; k < z; k++)
            {
                if (remove)
                {
                    *(ret + z * (y * i + j) + k) = (ARR_TYPE)0;
                }
                else
                {
                    *(ret + z * (y * i + j) + k) = *(n + z * (y * i + j) + k);
                }
            }
        }
    }
}
