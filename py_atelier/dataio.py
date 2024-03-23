import numpy as np
import pandas as pd
import random

prices_data = pd.read_csv("files/MP_M1_2009.csv")

# Deterministic division
# a) Total number of folds
# b) equally_sized = True

# random-over-random: Random folds, of random size

# a) Number of folds: 
# a.1) A random sample from a distribution (**parameters): 
#      default: Uniform, [2, max(10, n_obs//500]

n_obs = prices_data.shape[0]
rand = np.random.default_rng()

default_vals = ['uniform', 2, max(10, n_obs//500), 1]
uni_rand = rand.integers(
    low=default_vals[1], 
    high=default_vals[2], 
    size=default_vals[3], 
    endpoint=True, 
    dtype=np.int32)
n_folds = uni_rand[0]


# b) Size of each fold: 
# b.1) A random sampling process with selectable variance
# step 1: 

def divide_time_series(obs, folds, generator:str = 'normal'):
    total_indices = 0
    sub_datasets = []
    
    for _ in range(0, folds):
        
        if generator == 'constant':
            L = obs // folds
        
        elif generator == 'normal':
            mean_fold_size = max(total_indices, obs - total_indices) // folds
            var_fold_size = np.int32(mean_fold_size*0.5)
            L = random.normalvariate(mean_fold_size, var_fold_size) if folds > 1 else obs - total_indices
        
        # Define start and end indices for the sub-dataset
        end_index = total_indices + np.int32(L)
        sub_datasets.append([total_indices, end_index])
        
        # Update total_indices
        total_indices = end_index
        
        if total_indices == obs:
            break
    
    # the finel tuple always end at the last index
    sub_datasets[-1][1] = obs
    
    return sub_datasets

# Example usage:

sub_datasets = divide_time_series(obs=n_obs, folds=n_folds, generator='normal')
print("Sub-datasets:", len(sub_datasets))
