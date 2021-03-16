#include "utils.h"

using namespace std;

// To get greyscale value
float greyscale(vector<int> &pt){
    if (pt.size() != 3){
        throw length_error("Point is not RGB");
    }
    return pt[0]+pt[1]+pt[2];
}

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

//function to get the score of 2 pixels, with wb
float scorev2(vector<int> p1, vector<int> p2, float wr, float wg, float wb)
{
    if (p1.size() != p2.size())
    {
        throw length_error("Error calculating eculidean distance between unequal size arrays");
    }

    float res = (wr * abs(p1[0] - p2[0]) + wg * abs(p1[1] - p2[1]) + wb * abs(p1[2] - p2[2]))/(wr+wg+wb);

    return res;
}

float score_t_c(int i1, int j1, int i2, int j2, MAT3D &grid, MAT2D &lbp, float wr, float wg, float wb, float wc){
    vector<int> p1 = grid[i1][j1], p2 = grid[i2][j2];
    return wc * scorev2(p1, p2, wr, wg, wb) + (1 - wc) * abs(lbp[i1][j1] - lbp[i2][j2]);
}

// Fucntion to check the merging criteria
bool matchLbp(int i1, int j1, int i2, int j2, MAT3D &grid, int thres, MAT2D &lbp, float wr, float wg, float wb, float wc)
{
    float diff = score_t_c(i1, j1, i2, j2, grid, lbp, wr, wg, wb, wc);
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
