
# -- 

import pandas as pd
import numpy as np
from scipy.stats import kurtosis as m_kurtosis
from scipy.stats import skew as m_skew

# --------------------------------------------------------------- ----------------- -- #
# --------------------------------------------------------------- ----------------- -- #

def to_array(X) -> np.ndarray:
    """
    """

    if isinstance(X, np.ndarray):
        return X
    
    elif isinstance(X, list):
        return np.array(X).flatten()

    elif isinstance(X, pd.DataFrame):
        return X.to_numpy().flatten()

    else: 
        raise TypeError(type(X), "is not a supported type for to_array()")

# --------------------------------------------------------------- ----------------- -- #
# --------------------------------------------------------------- ----------------- -- #

def data_scaler(X: np.array, method: str) -> list:
    """
    """
        
    X = to_array(X)
    
    if X.ndim == 1:
        
        if method == 'standard':
            ops = {'mean': np.mean(X), 'std': np.std(X)}
            vals = (X - ops['mean']) / ops['std']
            return [vals, ops]
        
        elif method == 'robust':
            ops = {'median': (X - np.median(X, axis=0)),
                   'iqr': (np.percentile(X, 75, axis=0) - np.percentile(X, 25, axis=0))}
            vals = ops['median']/ops['iqr']
            return [vals, ops]
        
        elif method == 'max_abs':
            ops = {'max_abs': np.max(np.abs(X), axis=0)}
            vals = X / ops['max_abs']
            return [vals, ops]


# --------------------------------------------------------------- DATA PRE-SCALLING -- #
# --------------------------------------------------------------- ----------------- -- #

def series_scaler(p_data, p_trans):
    """
    Estandarizar (a cada dato se le resta la media y se divide entre la desviacion estandar) se aplica a
    todas excepto la primera columna del dataframe que se use a la entrada

    Parameters
    ----------
    p_trans: str
        Standard: Para estandarizacion (restar media y dividir entre desviacion estandar)
        Robust: Para estandarizacion robusta (restar mediana y dividir entre rango intercuartilico)

    p_datos: pd.DataFrame
        Con datos numericos de entrada

    Returns
    -------
    p_datos: pd.DataFrame
        Con los datos originales estandarizados

    """

    # hardcopy of the data
    data = p_data.copy()
    # list with columns to transform
    lista = data[list(data.columns)]
    # choose to scale from 1 in case timestamp is present
    scale_ind = 1 if 'timestamp' in list(data.columns) else 0


    standard_scaler = lambda X: (X - np.mean(X, axis=0)) / np.std(X, axis=0)
    robust_scaler = lambda X: (X - np.median(X, axis=0)) / (np.percentile(X, 75, axis=0) - 
                                                            np.percentile(X, 25, axis=0))
    max_abs_scaler = lambda X: X / np.max(np.abs(X), axis=0)
    
    if p_trans == 'standard':
        
        # removes the mean and scales the data to unit variance
        data[list(data.columns[scale_ind:])] = standard_scaler().fit_transform(lista.iloc[:, scale_ind:])
        return data

    elif p_trans == 'robust':

        # removes the meadian and scales the data to inter-quantile range
        data[list(data.columns[scale_ind:])] = robust_scaler().fit_transform(lista.iloc[:, scale_ind:])
        return data

    elif p_trans == 'scale':

        # scales to max value
        data[list(data.columns[scale_ind:])] = max_abs_scaler().fit_transform(lista.iloc[:, scale_ind:])
        return data
    
    else:
        print('Error in data_scaler, p_trans value is not valid')


# ------------------------------------ EXPLORATORY DATA ANALYSIS & FEATURES METRICS -- #
# ------------------------------------ ----------------------------------------------- #

def series_profile(p_data, p_type, p_mult):
    """
    OHLC Prices Profiling (Inspired in the pandas-profiling existing library)

    Parameters
    ----------

    p_data: pd.DataFrame
        A data frame with columns of data to be processed

    p_type: str
        indication of the data type: 
            'ohlc': dataframe with TimeStamp-Open-High-Low-Close columns names
            'ts': dataframe with unknown quantity, meaning and name of the columns
    
    p_mult: int
        multiplier to re-express calculation with prices,
        from 100 to 10000 in forex, units multiplication in cryptos, 1 for fiat money based assets
        p_mult = 10000

    Return
    ------
    r_data_profile: dict
        {}
    
    References
    ----------
    https://github.com/pandas-profiling/pandas-profiling


    """

    # copy of input data
    f_data = p_data.copy()

    # interquantile range
    def f_iqr(param_data):
        q1 = np.percentile(param_data, 75, interpolation = 'midpoint')
        q3 = np.percentile(param_data, 25, interpolation = 'midpoint')
        return  q1 - q3
    
    # outliers function (returns how many were detected, not which ones or indexes)
    def f_out(param_data):
        q1 = np.percentile(param_data, 75, interpolation = 'midpoint')
        q3 = np.percentile(param_data, 25, interpolation = 'midpoint')
        lower_out = len(np.where(param_data < q1 - 1.5*f_iqr(param_data))[0])
        upper_out = len(np.where(param_data > q3 + 1.5*f_iqr(param_data))[0])
        return [lower_out, upper_out]

    # in the case of a binary target variable just print the ocurrences of each value (for imbalace)
    if p_type == 'target':
        return p_data.value_counts()

    # -- OHLCV PROFILING -- #
    elif p_type == 'ohlc':

        # initial data
        ohlc_data = p_data[['open', 'high', 'low', 'close', 'volume']].copy()

        # data calculations
        ohlc_data['co'] = round((ohlc_data['close'] - ohlc_data['open'])*p_mult, 2)
        ohlc_data['hl'] = round((ohlc_data['high'] - ohlc_data['low'])*p_mult, 2)
        ohlc_data['ol'] = round((ohlc_data['open'] - ohlc_data['low'])*p_mult, 2)
        ohlc_data['ho'] = round((ohlc_data['high'] - ohlc_data['open'])*p_mult, 2)

        # original data + co, hl, ol, ho columns
        f_data = ohlc_data.copy()
        
    # basic data description
    data_des = f_data.describe(percentiles=[0.25, 0.50, 0.75, 0.90])

    # add skewness metric
    skews = pd.DataFrame(m_skew(f_data)).T
    skews.columns = list(f_data.columns)
    data_des = data_des.append(skews, ignore_index=False)

    # add kurtosis metric
    kurts = pd.DataFrame(m_kurtosis(f_data)).T
    kurts.columns = list(f_data.columns)
    data_des = data_des.append(kurts, ignore_index=False)
    
    # add outliers count
    outliers = [f_out(param_data=f_data[col]) for col in list(f_data.columns)]
    negative_series = pd.Series([i[0] for i in outliers], index = data_des.columns)
    positive_series = pd.Series([i[1] for i in outliers], index = data_des.columns)
    data_des = data_des.append(negative_series, ignore_index=True)
    data_des = data_des.append(positive_series, ignore_index=True)
    
    # index names
    data_des.index = ['count', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'p90',
                      'max', 'skew', 'kurt', 'n_out', 'p_out']

    return np.round(data_des, 2)

