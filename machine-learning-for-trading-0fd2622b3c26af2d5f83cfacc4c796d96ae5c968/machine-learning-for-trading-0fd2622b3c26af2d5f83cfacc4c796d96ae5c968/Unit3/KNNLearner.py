"""The implementation of the K Nearest Neighbors learner used to predict future stock prices
Note that this can be applied to many other datasets as well"""

import numpy as np
import math

class KNNLearner(object):
    k = 1
    storedVals = ''

    def __init__(self, k):
        KNNLearner.k = k
        pass

    """Adds training data to the learner. Takes as input the X and Y training values to train over"""
    def addEvidence(self,dataX,dataY):
        KNNLearner.storedVals = dataX.copy()
        KNNLearner.storedVals['y_vals'] = dataY
        KNNLearner.storedVals['y_vals'] = KNNLearner.storedVals['y_vals'].fillna(method='ffill')
        return
        
        
    """Estimates a set of test points using the model built in the method above.
    takes as input a numpy array with each row corresponding to the index you want to query.
    Returns the value that the model estimates for those points"""
    def query(self,points):
        KNNLearner.storedVals['distances'] = 0
        points['predicted_vals'] = 0
        KNNLearner.storedVals['normed_prices'] = KNNLearner.storedVals['actual_prices']/KNNLearner.storedVals.iloc[0,0] -1
        points['normed_prices'] = points['actual_prices']/points.iloc[0,0] -1
        points = points.fillna(method='ffill')
        points = points.fillna(method='bfill')
        KNNLearner.storedVals = KNNLearner.storedVals.fillna(method='ffill')
        KNNLearner.storedVals = KNNLearner.storedVals.fillna(method='bfill')

        for i in range (0, len(points.index)):
            KNNLearner.storedVals['distances'] = np.sqrt((KNNLearner.storedVals['bb_value'] - points.iloc[i,1]) **2 ) + np.sqrt((KNNLearner.storedVals['momentum'] - points.iloc[i,2])**2) + np.sqrt((KNNLearner.storedVals['volatility'] - points.iloc[i,3])**2) + np.sqrt((KNNLearner.storedVals['normed_prices'] - points.iloc[i,5]) **2 )
            sortedDistances = KNNLearner.storedVals.sort(['distances'])
            kmean = np.mean(sortedDistances.iloc[:KNNLearner.k,4])
            points.iloc[i,4] = kmean

        points['predicted_vals'] = points['predicted_vals'] + (points.iloc[0,0] - KNNLearner.storedVals.iloc[0,0])
        return points['predicted_vals']
