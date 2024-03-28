
import itertools

# -------------------------------------------------------- Search Space Calculation -- # 
# ------------------------------------------------------------------------------------ #

def search_space(dimensions:list) -> list:
    """
    Takes a dictionary of lists, where each key is a dimension, and where the value 
    for each key is the list of values that can be observed in the dimension. 

    Parameters:
    ----------

    dimensions: dict
        where each key is the dimension, and each of the respective values for the keys
        are the range of values that can be used for each dimension.

    Returns:
    --------
    
    l_space: list
        contains all the possible combinations of dimensions and values.

    Examples:
    --------
    
    experiment_1 = {'hyperparam_1': ['h1_1', 'h1_2', 'h1_3'],
                    'hyperparam_2': ['h2_1'],
                    'hyperparam_3': ['h3_1', 'h3_2'],
                    }

    search_space(dimensions=experiment_1)    

    """

    l_space = list(itertools.product(*[dimensions['hyperparameter_1'],
                                       dimensions['hyperparameter_2'],
                                       dimensions['hyperparameter_3']]
                                    ))

    return l_space
