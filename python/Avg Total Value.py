# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 20:24:03 2018

@author: harry
"""

import datetime as dt 
import pandas_datareader.data as web
import numpy as np

output = []
def total_volume(num_stocks):
    global output
    year = int(dt.datetime.today().strftime('%Y'))
    day = int(dt.datetime.today().strftime('%d'))
    month = int(dt.datetime.today().strftime('%m'))
    start = dt.datetime(2018,1,1)
    end = dt.datetime(year, month, day)
    for k in range(num_stocks):
        a = input("Enter your stock")
        b = int(input("Enter volume of stock"))
        df = web.DataReader(a, 'yahoo', start, end)
        df1 = df[['Close']]
        data = df1.values
        closing = []
        
        for i in range(len(data)):
            closing.append(float(data[i]*b))
        avg = np.mean(closing)
        output.append(avg)
    print(output)
    
   
    