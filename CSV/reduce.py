# this file is to reduce the dataset to our choice of size with the same distribution as the original dataset.


import pandas as pd
import numpy as np
import math

orig = pd.read_csv("only_names_and_label.csv")


classes = orig.classification.unique()


# remove rows with value as viable:non-viable
orig = orig[orig.classification != classes[len(classes) - 1]]
classes = orig.classification.unique()

# find the count of each class
count = list()
for cls in classes:
    tmp = orig[orig.classification == cls]

    count.append(tmp.shape[0])

# count stores the count of rows for each class
print(count, classes)

# number of items in the new dataset
# proportion of each class in the original dataset
proportion = count/np.sum(count)

size_new_dataset = 10

# count of each class in new dataset
count_new = [math.ceil(x) for x in proportion*size_new_dataset]

# randomly sample items from the original dataset with the same dist and the given column name
final_dataset = pd.DataFrame(columns=orig.columns)
for i in range(len(count_new)):
    tmp = orig[orig.classification == classes[i]].sample(n=count_new[i])
    final_dataset = final_dataset.append(tmp)

print(final_dataset)

# save the dataframe as csv file
final_dataset.to_csv("reduced.csv")

# rd = pd.read_csv("reduced.csv")
# print(rd)
