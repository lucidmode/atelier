# 
from math import log
import numpy as np
from scipy.special import gamma
from scipy.optimize import minimize

# --------------------------------------------------- Draw a sample from a Gamma PDF -- #
# ------------------------------------------------------------------------------------- #

def gamma_pdf(x:float, params:list[float, float]) -> float:
    """
    """

    alpha, beta = params[0], params[1]

    return (beta**alpha * x**(alpha - 1) * np.exp(-beta * x)) / gamma(alpha)

# ---------------------------------------------------- Fit Parameters to a Gamma PDF -- #
# ------------------------------------------------------------------------------------- #

def gamma_params(data, method='MoM') -> dict:
    """
    Computes the parameters of a gamma probability density function (pdf), according to the selected
    method.

    Parameters
    ----------

    data: np.array
        The data with which will be adjusted the pdf
    
    method: str
        Method to calculate the value of the parameters for the pdf
            'MoM': Method of Moments (Default)

    Returns
    -------

    r_params: dict
        {'alpha': gamma distribution paramerter, 'beta': gamma distribution parameter}
    
    """

    # -- Methods of Moments -- #
    if method == 'MoM':

        # first two moments
        mean = np.mean(data)
        variance = np.var(data)
        # sometimes refered in literature as k
        alpha = mean**2/variance
        # sometimes refered in literature as 1/theta
        beta = mean/variance
    
    elif method == 'MLE':
        
        # total number of observations
        n = len(data)
    
        # Calculate shape parameter
        alpha = n / sum(log(x) for x in data) - sum(log(x) for x in data) / n

        # Calculate scale parameter
        beta = n / sum(data)
    
    elif method == 'LS':

        # Define objective function
        def objective(params):
            return sum((x - gamma_pdf(x, params))**2 for x in data)

        # Initial guess for parameters
        initial_guess = [1.0, 1.0]  # initial guess for alpha and beta

        # Minimize the objective function
        result = minimize(objective, initial_guess, method='Nelder-Mead')

        # Extract estimated parameters
        alpha, beta = result.x
    
    # -- For errors or other unsupported methods
    else:
        raise ValueError("Currently, the supported methods are: ['MoM', 'MLE', 'LS']")

    # return the gamma distribution empirically adjusted parameters
    return {'alpha': alpha, 'beta': beta}
