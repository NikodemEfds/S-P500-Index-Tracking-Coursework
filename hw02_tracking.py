"""

Homework 2 - Part 2
Instructions in index_tracking.md
You may import additional libraries for this part
The os and pandas libraries below are required

"""
import os
import numpy as np
from scipy.optimize import minimize
import pandas as pd

def index_tracking_cleaning():
    """
    Process securities and index data for index tracking.

    Removes securities with any NA observations, calculate returns for
    both datasets, combines them, drops rows with NA values introduced by
    the return calculation, and splits into train and test sets.

    Returns:
        tuple: (train_df, test_df) where each is a DataFrame

    Example use:
    >>> ret_val = index_tracking_cleaning()
    >>> len(ret_val)
    2
    >>> train, test = index_tracking_cleaning()
    >>> isinstance(train, pd.DataFrame)
    True
    >>> 'SNDK' not in train.Ticker.unique()
    True
    >>> "return" in train.columns.str.lower()
    True
    >>> "^GSPC" in train.Ticker.unique()
    True
    >>> "2025-05-22" in pd.to_datetime(train.Date.unique())
    True
    """
    # Loading data from CSV files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df_securities = pd.read_csv(os.path.join(current_dir, "sp500_securities_23_25.csv"))
    df_index = pd.read_csv(os.path.join(current_dir, "sp500_index_23_25.csv"))
    # DO NOT CHANGE ANYTHING ABOVE. Your code starts below.
    #check whether there are any NAs if there are we flag the ticker as bad
    bad_tickers = df_securities[df_securities.isna().any(axis=1)]['Ticker'].unique()
    #keep only those NOT in bad tickers
    securities = df_securities[~df_securities['Ticker'].isin(bad_tickers)]
    #Create a new column for returns, group it by the ticket name and take the percentage change of close
    securities["Return"] = securities.groupby("Ticker")["Close"].pct_change()
    index = df_index
    index["Return"] = index.groupby("Ticker")["Close"].pct_change()
    #merge the data sets by STACKING merging messes it up
    combo = pd.concat([securities, df_index], axis=0)
    combo = combo.dropna()
    combo = combo.sort_values("Date")
    #make a split point between test data and train data, take all the data up to 80 then all the data after
    eightyPercent = int(len(combo) * 0.8)
    train_df = combo.iloc[: eightyPercent]
    test_df = combo.iloc[eightyPercent:]
    #print(combo.head())
    return train_df, test_df



def full_index_tracking():
    """
    Full index tracking as per Q1b).

    Returns:
        dict: Ticker (string) -> weight (float).

    Example use:
    >>> weights = full_index_tracking()
    >>> isinstance(weights, dict)
    True
    >>> all(isinstance(k, str) for k in weights.keys())
    True
    >>> all(isinstance(v, float) for v in weights.values())
    True
    >>> all(v >= -1e-5 for v in weights.values())
    True
    >>> float(round(sum(weights.values()), 2))
    1.0
    """
    train, test = index_tracking_cleaning()
    # DO NOT CHANGE ANYTHING ABOVE. Your code starts below.
    #rotate the data frame to wide so we can compare columns against eachother
    wideTraining = train.pivot(index = "Date", columns = "Ticker", values = "Return").fillna(0)
    #manipulate the data frames into values used for the calc
    r = wideTraining["^GSPC"].values
    XDF = wideTraining.drop(columns = ["^GSPC"])
    X = XDF.values
    T = len(r)
    numAssets = X.shape[1]

    
    #objective function to calculate ete
    def targetFunction(w):
    
        portfolioReturn = (X) @ w
        targetIndex = (r)
    
        errors = portfolioReturn - targetIndex
             
        ete = (np.sum(errors**2) / T) 
        return ete

    #sum of weights - 1 must equal 0, fancy way of writing it in the maths format
    #type is equation, function is lambda where the sum of w -1 must equal 0
    constraints = ({"type":"eq", "fun" : lambda w :np.sum(w) - 1})

    #weight must be greater than 0 and less than 1
    bounds = [(0,1) for i in range(numAssets)]
    
    #since the algorithm is iterative we need a starting point, so lets assume all weights are equal
    initialW = np.array([1/numAssets] * numAssets)

    #optimisation algorithm is SLSQP which is sequential least squares programming
    #not sure what that is but its an optimisation algorithm which follows the objective we set, the starting point
    # and the bounds and constraints we set.
   #NEW I added a tolerance function to make it consider very small changes as originally it was happy with the starting w so i made it more sensitive

    optimum = minimize(
    targetFunction, 
    initialW, 
    method="SLSQP", 
    bounds=bounds, 
    constraints=constraints,
    tol=1e-15,            
    options={'ftol': 1e-15} 
)

  

    #dictionary linked to an array of weights
    weightsDictionary = dict(zip(XDF.columns, optimum.x))
    sortedTuples = sorted(weightsDictionary.items(), key=lambda x: x[1], reverse=True)
    
    finalWeights = {str(k): float(v) for k, v in sortedTuples}

    

    #print(finalWeights)
    #literally doing the same thing i did to train minus the calculation
    wideTest = test.pivot(index="Date", columns="Ticker", values="Return").fillna(0)
    rTest = wideTest["^GSPC"].values
    XTest = wideTest.drop(columns=["^GSPC"]).values
    TTest = len(rTest)

    portfolioReturnTest = XTest @ optimum.x 
    errorsTest = portfolioReturnTest - rTest
    eteTest = np.sum(errorsTest**2) / TTest

    #results of ESE
    #print(optimum.fun)
    #print(eteTest)
    return finalWeights


def efficient_index_tracking():
    """
    Efficient index tracking with at most 50 non-zero weights as per Q2a).

    Returns:
        dict: Ticker (string) -> weight (float) with at most 50 non-zero entries.

    Example use:
    >>> weights = efficient_index_tracking()
    >>> isinstance(weights, dict)
    True
    >>> all(isinstance(k, str) for k in weights.keys())
    True
    >>> all(isinstance(v, float) for v in weights.values())
    True
    >>> all(v >= -1e-5 for v in weights.values())
    True
    >>> bool(sum(abs(v) > 1e-10 for v in weights.values()) <= 50)
    True
    >>> float(round(sum(weights.values()), 2))
    1.0
    """
    train, test = index_tracking_cleaning()
    # DO NOT CHANGE ANYTHING ABOVE. Your code starts below.
        #rotate the data frame to wide so we can compare columns against eachother
    wideTraining = train.pivot(index = "Date", columns = "Ticker", values = "Return").fillna(0)
    #manipulate the data frames into values used for the calc
    r = wideTraining["^GSPC"]
    XDF = wideTraining.drop(columns = ["^GSPC"])

    #use corrwith to find the correlation between the index individual stocks, we need it in absolute because the correlation could be negative
    correlatedAssets = XDF.corrwith(r).abs()
    #sort the top 50 values by correlation
    sortedCorrelatedAssets = correlatedAssets.sort_values(ascending = False)
    top50 = sortedCorrelatedAssets.sort_values(ascending = False).head(50).index

    #adjust the variables around the new data set
    rValues = r.values
    XDF50 = XDF[top50]
    X = XDF50.values
    T = len(rValues)
    numAssets = 50

    
    #objective function to calculate ete
    def targetFunction(w):
    
        portfolioReturn = (X) @ w
        targetIndex = (r)
    
        errors = portfolioReturn - targetIndex
             
        ete = (np.sum(errors**2) / T) 
        return ete

    #sum of weights - 1 must equal 0, fancy way of writing it in the maths format
    #type is equation, function is lambda where the sum of w -1 must equal 0
    constraints = ({"type":"eq", "fun" : lambda w :np.sum(w) - 1})

    #weight must be greater than 0 and less than 1
    bounds = [(0,1) for i in range(numAssets)]
    
    #since the algorithm is iterative we need a starting point, so lets assume all weights are equal
    initialW = np.array([1/numAssets] * numAssets)

    #optimisation algorithm is SLSQP which is sequential least squares programming
    #not sure what that is but its an optimisation algorithm which follows the objective we set, the starting point
    # and the bounds and constraints we set.
   #NEW I added a tolerance function to make it consider very small changes as originally it was happy with the starting w so i made it more sensitive

    optimum = minimize(
    targetFunction, 
    initialW, 
    method="SLSQP", 
    bounds=bounds, 
    constraints=constraints,
    tol=1e-15,            
    options={'ftol': 1e-15} 
)

  

    #dictionary linked to an array of weights
    #adjust the top 50
    weightsDictionary = dict(zip(top50, optimum.x))
    #make a dictionary
    sortedTuples = sorted(weightsDictionary.items(), key=lambda x: x[1], reverse=True)
    finalWeights = {str(k): float(v) for k, v in sortedTuples}
   
    #print(finalWeights)
    #literally doing the same thing i did to train minus the calculation
    wideTest = test.pivot(index="Date", columns="Ticker", values="Return").fillna(0)
    rTest = wideTest["^GSPC"].values
    #adjust for top 50 for test data
    XTest50 = wideTest[top50].values
    TTest = len(rTest)
    #adjust for new data
    portfolioReturnTest = XTest50 @ optimum.x 
    errorsTest = portfolioReturnTest - rTest
    eteTest = np.sum(errorsTest**2) / TTest

    #results of ESE
    #print(optimum.fun)
    #print(eteTest)
    return finalWeights
