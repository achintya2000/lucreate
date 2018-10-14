# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 15:59:34 2018

@author: harry
"""

import pandas as pd
import datetime as dt 
import pandas_datareader.data as web
import numpy as np 
import time as t
import matplotlib.pyplot as plt


start = dt.datetime(2018,5,1)
end = dt.datetime(year, month, day)
df = web.DataReader('TSLA', 'yahoo', start, end)
#print(df)
df1 = df[['Close']]
data = df1.values
print(data)
roc = []

for k in range(len(data)-1):
    roc += list(np.log(data[k]/data[k+1]))




#%% avg, stdv, variance, drift

#for j in range(len(roc)):
#    total = 0
#    total += roc[k]
#    avg = total/len(roc)
avg = np.mean(roc)
variance = np.std(roc)**2
standard_de = np.std(roc)
drift = avg - (variance/2)


#%%

def equation_test(runs=1):
    close=data[len(data)-1]
    predicts = []
    while runs>0:
        new_close = float(close*np.exp(drift+standard_de*np.random.uniform(0.0001,1)))
        runs -= 1
        print(new_close)
        predicts.append(new_close)
        close = new_close       
    return predicts

a = range(len(data))
plt.plot(a,data)
for n in range(100):
    b = range(len(data),len(data)+20)
    plt.figure(1)
    plt.plot(b, equation_test(20))
        
    
