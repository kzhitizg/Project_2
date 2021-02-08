#include "NbrRegionSegment.h"
// #include <bits/stdc++.h>

using namespace std;

// To add a region mapping to the table
void add(map<int, int> &eqtable, int v1, int v2)
{
    int mn = min(v1, v2);
    int mx = max(v1, v2);
    if ((eqtable).find(mx) != (eqtable).end() && (eqtable)[mx] != mn)
        add(eqtable, mn, (eqtable)[mx]);
    (eqtable)[mx] = mn;
}

// Function to Calculate the euclidean distance between two same size vectors
float norm(vector<int> &p1, vector<int> &p2)
{
    if (p1.size() != p2.size())
    {
        throw length_error("Error calculating eculidean distance between unequal size arrays");
    }

    float res = 0;

    for (int i = 0; i < p1.size(); i++)
    {
        res += pow(p1[i] - p2[i], 2);
    }
    return sqrt(res);
}

// Fucntion to check the merging criteria
bool match(int i1, int j1, int i2, int j2, MAT3D &grid, int thres)
{
    vector<int> p1 = grid[i1][j1], p2 = grid[i2][j2];
    if (norm(p1, p2) < thres)
        return true;
    return false;
}

//function to get the score of 2 pixels
float score(vector<int> p1, vector<int> p2, float wr, float wg)
{
    if (p1.size() != p2.size())
    {
        throw length_error("Error calculating eculidean distance between unequal size arrays");
    }

    float res = wr * abs(p1[0] - p2[0]) + wg * abs(p1[1] - p2[1]) + (1 - wr - wg) * abs(p1[2] - p2[2]);

    return res;
}

// Fucntion to check the merging criteria
bool matchLbp(int i1, int j1, int i2, int j2, MAT3D &grid, int thres, MAT2D &lbp, float wr, float wg, float wc)
{
    vector<int> p1 = grid[i1][j1], p2 = grid[i2][j2];
    float diff = wc * score(p1, p2, wr, wg) + (1 - wc) * abs(lbp[i1][j1] - lbp[i2][j2]);
    if (diff < thres)
        return true;
    return false;
}

// Function to print the bar
void bar(int part, int total)
{
    int barWidth = 70;
    float progress = ((float)part) / total;

    std::cout << "[";
    int pos = barWidth * progress;
    for (int i = 0; i < barWidth; ++i)
    {
        if (i < pos)
            std::cout << "=";
        else if (i == pos)
            std::cout << ">";
        else
            std::cout << " ";
    }
    std::cout << "] " << part << " / " << total << "\r";
    std::cout.flush();

    progress += 0.16; // for demonstration only
}

int shouldRemove(vector<int> vals)
{
    unordered_map<int, int> mp;

    for (auto &&i : vals)
    {
        // cout << (mp[i]) << endl;
        mp[i]++;
    }

    for (auto &&i : mp)
    {
        if (i.second > 5)
        {
            // del mp;
            return i.first;
        }
    }
    return -1;
}

void removeNoise(vector<vector<int>> &lbl)
{
    vector<int> vals(9, 0);
    int c = 0, v;
    int total = 0;
    for (int i = 1; i < lbl.size() - 1; i++)
    {
        for (int j = 1; j < lbl[0].size() - 1; j++)
        {
            // total += 1;
            // if (total % 10000 == 0){

            //     bar(total , (lbl.size()*lbl[0].size()));
            // }
            fill(vals.begin(), vals.end(), 0);
            c = 0;
            for (int a = i - 1; a <= i + 1; a++)
            {
                for (int b = j - 1; b <= j + 1; b++)
                {
                    vals[c++] = lbl[a][b];
                }
            }

            v = shouldRemove(vals);
            if (v != -1)
            {
                lbl[i][j] = v;
            }
        }
    }
}

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
vector<vector<int>> labelv2(MAT3D &grid, int thres, MAT2D &lbp, float wr = 0.2, float wg = 0.2, float wc = 0.7)
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
            if ((i > 0 && matchLbp(i, j, i - 1, j, grid, thres, lbp, wr, wg, wc)) && (j > 0 && matchLbp(i, j, i, j - 1, grid, thres, lbp, wr, wg, wc)))
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

// Function to be exported. Takes image array as input and returns image with coloured regions
void segment(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres, float wr, float wg, float wc, ARR_TYPE *ret)
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

    vector<vector<int>> lbl = labelv2(img, thres, lbp, wr, wg, wc);

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

int getRegions(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres, float w, int *ret, int *count)
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

    vector<vector<int>> lbl = labelv2(img, thres, lbp, w);

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

void removeMap(int *n, int x, int y, int thres, int *count, int regs, bool *ret)
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

void segmentAndRemove(ARR_TYPE *n, ARR_TYPE *l, int x, int y, int z, int thres1, int thres2, float w, ARR_TYPE *ret)
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

    vector<vector<int>> lbl = labelv2(img, thres1, lbp, w);

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