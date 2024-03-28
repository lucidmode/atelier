#

import numpy as np
import random 
import itertools

from py_atelier.dataio import prices_data

# ------------------------------------------------------------------ Folds Creation -- # 
# ------------------------------------------------------------------------------------ #

# -- Folds creation

# By Random division of the subsets
# By equally-spaced periods of time
# By Information Criteria

# -- Definitions

# len_data: data series length
# n_folds: number of folds
# len_fold: fold size

# -- Proces: Determination of the number of folds and/or size for each of the folds.

# A) Number of folds provided: 
#   The number of folds is provided, then the size for each fold is derived
    # 1) Deterministically
    # The user provides a fixed number of folds then size for each is calculated in 
    # equal divisions and the last fold might contain residuals.

    # 2) Probabilistic
    # The user provides the probability distribution name, parameters and no. of samples
    # so to get a known no. of folds then size for each is calculated in 
    # equal divisions and the last fold might contain residual.

# B) Fold size provided:
#   The fold sizes is provided, then the number of folds is derived.

    # 1) Deterministically
    # The user provides a fixed size to be used for all folds then number of folds is derived
    # in case of residuals, the last fold might contain residuals.

    # 2) Probabilistic
    # The user provides the probability distribution name, parameters and no. of samples
    # so to get a known size for the folds, then the total no. of folds is derived.

# C) Information based
# A range of min and max values, for either No. of Folds, or, size for each fold is required. 

#   1) Divide in 3
#   1) Fit a Generalized Gamma PDF with MoM

# --- Proces: Execution mode

    # 1) one-setp:
    # Calculations are done at once 

    # 2) sequential-step
    # either for A) and B), each drawn of value precludes a recalculation of the size of data to
    # produce the folds from.

# random-over-random: Random folds, of random size

# a) Number of folds: 
# a.1) A random sample from a distribution (**parameters): 
#      default: Uniform, [2, max(10, n_obs//500]

len_data = prices_data.shape[0]

rand = np.random.default_rng()
default_vals = ['uniform', 2, max(10, len_data//500), 1]
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
