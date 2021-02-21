#include "utils.h"

#include "Fitness.h"

using namespace std;

float IntraSegVariance(ARR_TYPE *n, int *labelled, int x, int y, int numReg)
{
    vector<vector<float>> img(x, vector<float>(y, 0));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            img[i][j] = *(n + (y * i + j))/256.0;
        }
    }

    vector<float> sum(numReg, 0.0);
    vector<double> count(numReg, 0.0);

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            sum[*(labelled + y * i + j)] += img[i][j];
            count[*(labelled + y * i + j)] += 1.0;
        }
    }

    vector<float> mean(numReg, 0);
    vector<float> countsq(numReg, 0);

    for (int i = 0; i < numReg; i++)
    {
        mean[i] = sum[i] / count[i];
        countsq[i] = count[i]*count[i];
    }

    vector<double> x_minus_x_bar(numReg, 0);

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            x_minus_x_bar[*(labelled + y * i + j)] += pow(img[i][j] - mean[*(labelled + y * i + j)], 2);
        }
    }

    /*
        variance of i-th region
        
        variance = x_minus_x_bar[i]/count[i];
        netvariance += count[i] * variance;

        So can be written as
        netvariance += x_minus_x_bar[i]
    */

    // 0.0 because result shoud be float
    double num = accumulate(x_minus_x_bar.begin(), x_minus_x_bar.end(), 0.0),
        // denom = numReg*numReg;
        denom = (((double)x)*numReg);

    // cout << num << ' ' << denom << endl;

    float net_variance = 10*num/denom;

    return (float)net_variance;
}

float MoranI(ARR_TYPE *n, int *labelled, int x, int y, int numReg)
{
    MAT2D img(x, vector<int>(y, 0));
    MAT2D lab(x, vector<int>(y, 0));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            img[i][j] = (int)*(n + (y * i + j));
        }
    }

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            lab[i][j] = *(labelled + (y * i + j));
        }
    }

    int nbrcount = 0;

    vector<set<int>> w(numReg, set<int>());

    // No need to consider right and down neighbours, as they will be counter later
    // Instead, 
    int dx[] = {0, -1};
    int dy[] = {-1, 0};

    //Calculation of the weights, wij
    //Calculation of mean of each region
    vector<float> sum(numReg, 0);
    vector<double> count(numReg, 0);
    float img_mean = 0;

    int a, b, r1, r2;

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            sum[lab[i][j]] += img[i][j];
            count[lab[i][j]] += 1;
            img_mean += img[i][j];

            for (int p = 0; p < 2; p++)
            {
                a = i + dx[p];
                b = j + dy[p];
                try
                {
                    r1 = min(lab.at(a).at(b), lab.at(i).at(j));
                    r2 = max(lab.at(a).at(b), lab.at(i).at(j));

                    if (w[r1].find(r2) == w[r1].end() && r1 != r2)
                    {
                        nbrcount += 1;
                        w[r1].insert(r2);
                    }
                }
                catch (const std::out_of_range &e)
                {
                }
            }
        }
    }

    img_mean /= x * y;

    // cout << "(cpp) Image mean = " << img_mean << ' ' << nbrcount << endl;

    vector<float> mean(numReg, 0);

    for (int i = 0; i < numReg; i++)
    {
        mean[i] = sum[i] / count[i];
    }

    float numerator = 0;
    set<int> *tmp;

    for (int i = 0; i < numReg; i++)
    {
        numerator += (mean[i] - img_mean) * (mean[i] - img_mean);
        for (int j = i+1; j < numReg; j++)
        {
            tmp = &w[i];

            if ((*tmp).find(j) != (*tmp).end())
            {
                numerator += (mean[i] - img_mean) * (mean[j] - img_mean);

            }
        }

        if (i % 1000 == 0)
        {
            bar(i, numReg);
        }
    }

    cout << endl;

    numerator *= numReg;

    float denominator = 0;

    for (int i = 0; i < numReg; i++)
    {
        denominator += pow(mean[i] - img_mean, 2);
    }

    denominator *= nbrcount;

    // cout << numerator << ' ' << denominator << endl;
    /*
        variance of i-th region
        
        variance = x_minus_x_bar[i]/count[i];
        netvariance += count[i] * variance;

        So can be written as
        netvariance += x_minus_x_bar[i]
    */

    return numerator / denominator;
}