#include "utils.h"

#include "Fitness.h"

using namespace std;

float IntraSegVariance(ARR_TYPE *n, int *labelled, int x, int y, int numReg){
    MAT2D img(x, vector<int>(y,0));

    // To compensate the labels being 1 based indexed
    // numReg++;

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