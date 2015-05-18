# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:00:03 2015

@author: daviz
"""

import pandas as pd
import statsmodels.api as sm
import numpy as np
import pylab
import seaborn as sns
#from datetime import datetime
#from sklearn import linear_model

ice = pd.read_csv("SeaIce.txt", delim_whitespace=True)
# Removing outliers
ice = ice[~(np.abs(ice.extent - ice.extent.mean()) > 3* ice.extent.std())]

# sorting by year and date and then using index as month counter
ice.sort(["year","mo"], inplace=True)
ice.reset_index(inplace = True)

#ice['date'] = ice.apply(lambda row: datetime(row['year'], row['mo'], 1), axis=1)
#ice = ice[["extent", "date"]]
#ice.plot(x="date")

# moving average implemented with convolution for performance
def moving_average(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

ice["extent_moving_mean"] = moving_average(ice.extent, 10)    
pylab.plot(ice.index,ice.extent,".")
pylab.plot(ice.index, ice.extent_moving_mean,"r")
pylab.xlim(0, 422); pylab.xlabel("Months counts"); pylab.ylabel("Extent")

# Using seaborn to display the regression line
sns.lmplot("index", "extent_moving_mean", ice)


# Showing some lineal regression summary.
est = sm.OLS(ice.extent_moving_mean, ice.index)
est = est.fit()
print est.summary()
