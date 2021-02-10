#include "utils.h"

#include "Fitness.h"

using namespace std;

float IntraSegVariance(ARR_TYPE *n, int *labelled, int x, int y, int numReg){
    MAT2D img(x, vector<int>(y,0));

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            img[i][j] = (int)*(n + (y * i + j));
        }
    }

    vector<float> sum(numReg, 0);
    vector<int> count(numReg, 0);

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            sum[*(labelled + y*i + j)] += img[i][j];
            count[*(labelled + y*i + j)] += 1;
        }
        
    }
    
    vector<float> mean(numReg, 0);

    for (int i = 0; i < numReg; i++)
    {
        mean[i] = sum[i]/count[i];
    }
    
    vector<float> x_minus_x_bar(numReg, 0);

    for (int i = 0; i < x; i++)
    {
        for (int j = 0; j < y; j++)
        {
            x_minus_x_bar[*(labelled + y*i + j)] += pow(img[i][j] - mean[*(labelled + y*i + j)], 2);
        }
    }

    /*
        variance of i-th region
        
        variance = x_minus_x_bar[i]/count[i];
        netvariance += count[i] * variance;

        So can be written as
        netvariance += x_minus_x_bar[i]
    */
    
    float net_variance = accumulate(x_minus_x_bar.begin(), x_minus_x_bar.end(), 0.0) / 
                                    accumulate(count.begin(), count.end(), 0.0);
                                    // 0.0 because result shoud be float
    
    return net_variance;
    
}

float MoranI(ARR_TYPE *n, int *labelled, int x, int y, int numReg){
    MAT2D img(x, vector<int>(y,0));
    MAT2D lab(x, vector<int>(y,0));

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

    unordered_map<int, set<int>> w;

    int nbr[][2] = {
        -1, 0,
        0, -1,
    };

    vector<float> sum(numReg, 0);
    vector<int> count(numReg, 0);
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
                a = i+nbr[p][0];
                b = j+nbr[p][1];
                try
                {
                    r1 = min(lab.at(a).at(b), lab.at(i).at(j));
                    r2 = max(lab.at(a).at(b), lab.at(i).at(j));

                    if (r1 != r2){
                        w[r1].insert(r2);
                    }
                }
                catch(const std::out_of_range& e){

                }
            }
            
        }
    }

    img_mean /= x*y;

    // cout << "(cpp) Image mean = " << img_mean << endl;

    vector<float> mean(numReg, 0);

    for (int i = 0; i < numReg; i++)
    {
        mean[i] = sum[i]/count[i];
    }

    float numerator = 0;
    set<int> tmp;

    for (int i = 0; i < numReg; i++)
    {
        for (int j = i+1; j < numReg; j++)
        {
            tmp = w[i];
            if (tmp.find(j) != tmp.end()){
                numerator += (mean[i]-img_mean)*(mean[j]-img_mean);
            }
        }
        // cout << i << endl;
    }

    numerator *= numReg;

    float denominator = 0;

    for (int i = 0; i < numReg; i++)
    {
        denominator += pow(mean[i]-img_mean, 2);
    }
    
    denominator *= w.size();

    /*
        variance of i-th region
        
        variance = x_minus_x_bar[i]/count[i];
        netvariance += count[i] * variance;

        So can be written as
        netvariance += x_minus_x_bar[i]
    */
    
    return numerator / denominator;
}